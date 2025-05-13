# Setup the evaluation and explainability testing environment

Here is the setup guide for evaluation and explainability testing environment. If you want to observe the full pipeline service code, please take a look at [Borbann repository](https://github.com/Sosokker/borbann/tree/main/pipeline).

## Prerequisites

You need the following tools to run the evaluation and explainability testing environment

- Python 3.12
- Google Cloud SDK
- Vertex AI SDK
- UV

Also, you need to modify the code in `vertex.py` to point to your project ID and model name. Create your own model in Vertex AI platform first, using the `train-1.jsonl`, `train-2.jsonl`, `train-3.jsonl` as training data and `evluation.jsonl` as evaluation data.

## Setup

```bash
uv sync
```

## Evaluation

```bash
gcloud auth application-default login
uv run evaluate.py
```

## Explainability

```bash
gcloud auth application-default login
uv run explainability.py
```
