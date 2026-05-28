---
inclusion: always
---

# Migration rules for the bank-marketing prediction workshop

This workspace migrates a **fully local** bank-marketing XGBoost project (`notebooks/model_development.ipynb` — plain Python + scikit-learn + XGBoost, no SageMaker SDK at all) onto **Amazon SageMaker AI** using the SageMaker Python SDK v3 (`notebooks/model_development_sagemaker.ipynb`). Apply these rules when generating or modifying code.

## Source of truth

- The **local baseline** lives in `notebooks/model_development.ipynb`. It is fully local — no SageMaker — and is the "before" state participants compare against. Do not modify it.
- The **SageMaker target** lives in `notebooks/model_development_sagemaker.ipynb`. All migration work lands here and in `scripts/`.
- API patterns: `.kiro/steering/sagemaker-v3.md`.
- Notebook editing rules: `.kiro/steering/jupyter-notebook.md`.

## Workshop `.env` keys

`.env` uses boto3-canonical env-var names on the left so boto3 picks up credentials and region automatically (no bridging needed). The placeholder on the right of each line names the matching CloudFormation Output the participant pastes in:

| `.env` key | Paste value from CFN Output |
|---|---|
| `AWS_ACCESS_KEY_ID` | `AwsAccessKeyId` |
| `AWS_SECRET_ACCESS_KEY` | `AwsSecretAccessKey` |
| `SAGEMAKER_EXECUTION_ROLE` | `SagemakerExecutionRoleArn` |
| `S3_BUCKET_NAME` | `WorkshopBucketName` |
| `AWS_REGION` | (defaults to `us-east-1`) |

When generating notebook / script code, just call `load_dotenv()` and read the keys directly:

```python
import os
from dotenv import load_dotenv

load_dotenv()

required = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "SAGEMAKER_EXECUTION_ROLE", "S3_BUCKET_NAME"]
missing = [k for k in required if not os.environ.get(k)]
if missing:
    raise RuntimeError(f"Missing .env keys: {missing}")

execution_role_arn = os.environ["SAGEMAKER_EXECUTION_ROLE"]
bucket_name = os.environ["S3_BUCKET_NAME"]
region = os.environ.get("AWS_REGION", "us-east-1")
```

boto3 will pick up `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_REGION` from the environment without any explicit wiring.

## Do

- Use exactly the pinned versions in `requirements.txt`. Do not auto-bump.
- Keep `scripts/preprocessing.py`, `scripts/train.py`, `scripts/inference.py` as the entry points consumed by `ProcessingJob`, `ModelTrainer`, `ModelBuilder`. SageMaker containers expect a `__main__` shim — keep it.
- Use `tempfile` for any local extraction (the existing notebook pattern). Clean up after extraction.
- Upload raw data to `s3://<bucket>/bank-marketing-prediction/raw/`, processed splits to `…/processed/{train,validation,test}/`, training output to `…/training/`. Match the existing path structure exactly.
- For every SageMaker job, call `.wait(poll=30)` (the v3 method — there is no `wait_for_status`) so the notebook reads cleanly top-to-bottom.
- After `predictor.deploy(...)` in Lab 5, also include a clearly-labeled `predictor.delete_endpoint()` cell so participants don't leave billable endpoints running.

## Don't

- Don't modify `notebooks/model_development.ipynb` — it is the read-only local baseline.
- Don't import `sagemaker.estimator`, `sagemaker.xgboost`, `sagemaker.processing`, `sagemaker.model`, or `sagemaker.predictor` — these are SDK 2.x paths, removed in 3.x, and raise `ModuleNotFoundError`.
- Don't write `from sagemaker_core...` — the package name is `sagemaker-core` but it installs into `sagemaker/core/`. Use `from sagemaker.core.resources import ...`.
- Don't pass legacy channel dicts to `.fit()`. Use `trainer.train(input_data_config=[InputData(channel_name=...), ...])`.
- Don't port the local FastAPI serving code (`src/serving/`) into `notebooks/model_development_sagemaker.ipynb`. The local FastAPI app is part of the "before" baseline; the SageMaker target uses Inference Endpoints via `ModelBuilder`.
- Don't introduce new top-level dependencies without bumping `requirements.txt` deliberately.
- Don't generate notebook content as text concatenation — use the JSON cell structure rules in `.kiro/steering/jupyter-notebook.md`.

## Workshop pacing

The workshop's labs are sequenced 0 → introduction → 1 → setup → 2 → environment → 3 → processing → 4 → training → 5 → deployment. When a participant prompts you to add code, scope your output to the **current lab only** unless explicitly asked to do more. Do not pre-emptively add training code while they're still on processing.

## Output expectations

- Markdown cells preceding each new code cell should explain what the participant is about to run and why — keep it tight (1–2 sentences) and avoid restating the SageMaker docs.
- Code cells should be runnable end-to-end if all prior cells in the notebook have run.
- Print intermediate state where it helps debugging (S3 URIs, job names, status). Avoid `print(model)` or other dumps that obscure the cell's intent.
