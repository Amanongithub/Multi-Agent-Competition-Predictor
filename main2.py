import json
import os
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

DATABASE_FILE = Path("data/predictions.json")


# ============================================================
# DATABASE
# ============================================================

def save_prediction(result):
    DATABASE_FILE.parent.mkdir(exist_ok=True)

    if DATABASE_FILE.exists():
        try:
            data = json.loads(
                DATABASE_FILE.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(result)

    DATABASE_FILE.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )


# ============================================================
# COMMON AI PROMPT
# ============================================================

def build_prompt(question):

    return f"""
You are an AI competition prediction analyst.

User question:
{question}

Predict the most likely winner.

Return ONLY valid JSON in this format:

{{
    "prediction": "winner name",
    "confidence": 75,
    "reasoning": "Short explanation",
    "key_factors": [
        "factor 1",
        "factor 2",
        "factor 3"
    ]
}}

Rules:
- Confidence must be between 0 and 100.
- Give your own independent prediction.
- Keep reasoning short.
- Do not invent facts.
- Confidence is model-reported confidence, not a calibrated probability.
"""


# ============================================================
# GEMINI AGENT
# ============================================================

def gemini_agent(question):

    print("[INFO] Running Agent 1 - Gemini...")

    start = time.time()

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=build_prompt(question),
        config=types.GenerateContentConfig(
            temperature=0.7,
            response_mime_type="application/json"
        )
    )

    result = json.loads(response.text)

    latency = round(time.time() - start, 2)

    print(
        f"[OK] Agent 1 predicted: "
        f"{result['prediction']}"
    )

    return {
        "agent": "Agent 1",
        "provider": "Gemini",
        "model": GEMINI_MODEL,
        "prediction": result["prediction"],
        "confidence": float(result["confidence"]),
        "reasoning": result["reasoning"],
        "key_factors": result.get("key_factors", []),
        "latency_seconds": latency
    }


# ============================================================
# OPENROUTER AGENT
# ============================================================

def openrouter_agent(question):

    print("[INFO] Running Agent 2 - OpenRouter...")

    start = time.time()

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "user",
                "content": build_prompt(question)
            }
        ],
        temperature=0.7
    )

    result = json.loads(
        response.choices[0].message.content
    )

    latency = round(time.time() - start, 2)

    print(
        f"[OK] Agent 2 predicted: "
        f"{result['prediction']}"
    )

    return {
        "agent": "Agent 2",
        "provider": "OpenRouter",
        "model": OPENROUTER_MODEL,
        "prediction": result["prediction"],
        "confidence": float(result["confidence"]),
        "reasoning": result["reasoning"],
        "key_factors": result.get("key_factors", []),
        "latency_seconds": latency
    }


# ============================================================
# CONSENSUS
# ============================================================

def calculate_consensus(predictions):

    groups = {}

    for agent in predictions:

        winner = agent["prediction"].strip()

        key = winner.lower()

        if key not in groups:
            groups[key] = []

        groups[key].append(agent)

    # Most agents supporting the same winner
    winner_group = max(
        groups.values(),
        key=lambda group: len(group)
    )

    winner = winner_group[0]["prediction"]

    support = len(winner_group)

    average_confidence = (
        sum(
            agent["confidence"]
            for agent in winner_group
        )
        / support
    )

    return {
        "winner": winner,
        "support": f"{support}/{len(predictions)}",
        "average_confidence": round(
            average_confidence,
            2
        )
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("MULTI-AGENT COMPETITION PREDICTOR")
    print("=" * 70)

    question = input(
        "\nEnter your prediction question: "
    ).strip()

    if not question:
        print("Question cannot be empty.")
        return

    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY is missing from .env")
        return

    if not OPENROUTER_API_KEY:
        print("OPENROUTER_API_KEY is missing from .env")
        return

    print("\n[INFO] Starting prediction...")
    print(f"[INFO] Question: {question}")

    # Two independent agents
    agent1 = gemini_agent(question)
    agent2 = openrouter_agent(question)

    predictions = [
        agent1,
        agent2
    ]

    print("\n[INFO] Calculating consensus...")

    consensus = calculate_consensus(predictions)

    print(
        f"[OK] Consensus: "
        f"{consensus['winner']} "
        f"({consensus['support']})"
    )

    # Save everything
    result = {
        "prediction_id": str(uuid.uuid4()),
        "question": question,
        "agents": predictions,
        "consensus": consensus
    }

    save_prediction(result)

    print(
        "\n[OK] Prediction saved to "
        "data/predictions.json"
    )

    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("AGENT PREDICTIONS")
    print("=" * 70)

    for agent in predictions:

        print(
            f"\n{agent['agent']} | "
            f"{agent['provider']}"
        )

        print(
            f"Prediction : {agent['prediction']}"
        )

        print(
            f"Confidence : "
            f"{agent['confidence']:.1f}%"
        )

        print(
            f"Reasoning  : "
            f"{agent['reasoning']}"
        )

        print(
            f"Factors    : "
            f"{', '.join(agent['key_factors'])}"
        )

        print(
            f"Latency    : "
            f"{agent['latency_seconds']}s"
        )

    print("\n")
    print("=" * 70)
    print("FINAL CONSENSUS")
    print("=" * 70)

    print(
        f"Predicted Winner      : "
        f"{consensus['winner']}"
    )

    print(
        f"Agent Support         : "
        f"{consensus['support']}"
    )

    print(
        f"Average AI Confidence : "
        f"{consensus['average_confidence']:.2f}%"
    )

    print(
        "\nNote: AI confidence is model-reported "
        "confidence, not a calibrated probability."
    )

    print(
        f"\nPrediction ID: "
        f"{result['prediction_id']}"
    )


if __name__ == "__main__":
    main()