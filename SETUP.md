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

## Input data gathering

To get the input data from pipeline service, you need to run the pipeline service first.

```bash
git clone https://github.com/borbann-platform/backend-api.git
cd backend-api/pipeline

uv sync
uv run main.py
```

The navigate to `127.0.0.1:8000/docs` to see the API documentation.
In the swagger documentation, you follow these steps

1. Create a new pipeline with preferred configuration
2. Go to `/pipeline/{pipeline_id}/run` and run the pipeline
3. Wait for the pipeline to finish
4. Go to `/pipeline/{pipeline_id}/result` to get the result
5. Copy the result
