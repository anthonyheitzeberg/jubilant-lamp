# mini-llm-judge

A small LLM evaluation harness. It sends test questions to a model, scores each answer with a deterministic check and an LLM judge, and logs results to `results.jsonl`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install litellm pydantic python-dotenv
```

## Run

```bash
python main.py
```

By default it uses a local Ollama model (`ollama/llama3.2`), so Ollama must be running with that model pulled.

## Configuration

Set these in the environment or a `.env` file:

| Variable | Default | Purpose |
| --- | --- | --- |
| `EVAL_MODEL` | `ollama/llama3.2` | Model being evaluated (any [litellm](https://docs.litellm.ai/docs/providers) name) |
| `JUDGE_MODEL` | same as `EVAL_MODEL` | Model used by the LLM judge |
| `RESULTS_FILE` | `results.jsonl` | Output path |

For hosted models, also set the provider key, e.g. `OPENAI_API_KEY`.

## Layout

- `main.py` – sample cases and entry point
- `runner.py` – calls the model
- `judges.py` – deterministic and LLM judges
- `models.py` – `JudgeScore` schema
- `storage.py` – result logging and summary
