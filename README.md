# Multi-Agent Competition Predictor

A simple AI-powered competition prediction system that uses two independent AI agents to predict the winner of any competition or event.

## How It Works

The user enters one natural-language question:

```text
Who will win Asia Cup?
```

The question is independently sent to:

1. **Agent 1 — Gemini**
2. **Agent 2 — OpenRouter**

Each agent returns:

* Predicted winner
* Confidence score
* Reasoning
* Key factors

The system then compares both predictions and calculates a consensus.

```text
                 User Question
                       │
                       ▼
              ┌─────────────────┐
              │  Prediction App │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
        ┌───────────┐     ┌────────────┐
        │  Gemini   │     │ OpenRouter │
        │  Agent 1  │     │  Agent 2   │
        └─────┬─────┘     └──────┬─────┘
              │                  │
              └────────┬─────────┘
                       ▼
              ┌─────────────────┐
              │ Consensus Engine│
              └────────┬────────┘
                       ▼
                Final Prediction
                       │
                       ▼
             data/predictions.json
```

## Features

* Two independent AI agents
* Gemini integration
* OpenRouter integration
* Generic competition prediction
* Natural-language input
* AI confidence scores
* Reasoning and key factors
* Simple consensus engine
* JSON prediction history
* Simple CLI
* No database required
* No web framework required
* No logging framework required

## Example

Run:

```bash
python main.py
```

Enter:

```text
Who will win Asia Cup?
```

Example output:

```text
======================================================================
MULTI-AGENT COMPETITION PREDICTOR
======================================================================

Enter your prediction question: Who will win Asia Cup?

[INFO] Starting prediction...
[INFO] Question: Who will win Asia Cup?
[INFO] Running Agent 1 - Gemini...
[OK] Agent 1 predicted: India
[INFO] Running Agent 2 - OpenRouter...
[OK] Agent 2 predicted: India

[INFO] Calculating consensus...
[OK] Consensus: India (2/2)

======================================================================
AGENT PREDICTIONS
======================================================================

Agent 1 | Gemini
Prediction : India
Confidence : 78.0%
Reasoning  : India has a strong overall squad...
Factors    : Squad strength, recent form, experience
Latency    : 2.31s

Agent 2 | OpenRouter
Prediction : India
Confidence : 72.0%
Reasoning  : India appears to have the strongest...
Factors    : Batting depth, bowling, experience
Latency    : 3.02s

======================================================================
FINAL CONSENSUS
======================================================================

Predicted Winner      : India
Agent Support         : 2/2
Average AI Confidence : 75.00%
```

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd Agentpre
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create `.env` in the project root.

Copy the example:

```bash
copy .env.example .env
```

Then add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

GEMINI_MODEL=gemini-3.8-flash
OPENROUTER_MODEL=openrouter/free
```

Never commit `.env` to GitHub.

## Data Storage

Predictions are stored locally in:

```text
data/predictions.json
```

Each prediction contains:

```json
{
  "prediction_id": "unique-id",
  "question": "Who will win Asia Cup?",
  "agents": [
    {
      "agent": "Agent 1",
      "provider": "Gemini",
      "prediction": "India",
      "confidence": 78,
      "reasoning": "...",
      "key_factors": [
        "Squad strength",
        "Recent form"
      ]
    }
  ],
  "consensus": {
    "winner": "India",
    "support": "2/2",
    "average_confidence": 75
  }
}
```

## Consensus Logic

The system currently uses a simple consensus approach.

If both agents predict the same winner:

```text
India
India

Consensus = India
Support   = 2/2
```

If the agents disagree:

```text
India
Australia
```

the prediction supported by more agents wins.

With only two agents, a disagreement means there is no true majority, so the first prediction group is selected by the current simple implementation.

## AI Confidence

The confidence score is **model-reported confidence**.

It should not be interpreted as a statistically calibrated probability.

For example:

```text
Confidence: 80%
```

does not mean there is an objectively measured 80% probability that the team will win.

## Technology

* Python
* Google Gemini
* OpenRouter
* OpenAI Python SDK
* JSON
* python-dotenv

## Project Goal

This project demonstrates a simple multi-agent architecture where different AI providers independently analyze the same problem and a separate consensus layer combines their outputs.

## Future Improvements

Possible future versions could add:

* More AI agents
* Live sports/news data
* Team statistics
* Ranking data
* Evidence collection
* Weighted consensus
* Historical accuracy tracking
* Confidence calibration
* PostgreSQL
* Web dashboard
* Docker
* CI/CD
* Automated testing

## Disclaimer

Predictions are generated by AI models and are for demonstration and educational purposes. They should not be treated as guaranteed outcomes or financial advice.
