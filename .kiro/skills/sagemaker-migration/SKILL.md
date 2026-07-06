---
name: sagemaker-migration
description: Migrate any local Python ML project (Jupyter notebooks, scripts, framework-agnostic) to Amazon SageMaker AI using SageMaker Python SDK v3 — covering Processing, Training, and Inference. Use when the user asks to move local ML code to SageMaker, add ModelTrainer / ModelBuilder / ProcessingJob code, or upgrade legacy SageMaker SDK 2.x code to 3.x.
license: Apache-2.0
compatibility: Requires Python 3.10+ and sagemaker>=3.0. Designed for SageMaker AI in any AWS region. No Kiro-specific syntax — runs in any agentskills.io-compatible client (Kiro IDE/CLI, Claude Code, etc.).
metadata:
  author: aws-samples
  version: "1.2.0"
  sdk-target: sagemaker>=3.0
---

# SageMaker Migration Skill (SDK v3)

Use this skill when a user wants to take a local Python ML project — Jupyter notebooks, plain scripts, scikit-learn / XGBoost / PyTorch / TensorFlow, FastAPI / Flask serving, anything — and run its preprocessing, training, and inference on Amazon SageMaker AI using **SageMaker Python SDK v3**.

It works in two scenarios:

1. **Greenfield migration** — user has local code that doesn't yet use SageMaker; help them lift each phase (preprocessing → training → inference) onto SageMaker using v3 patterns.
2. **Legacy upgrade** — user has older SageMaker code written against SDK 2.x and needs to update it to 3.x without losing behavior.

This skill is **portable** — it follows the [agentskills.io](https://agentskills.io) standard. No Kiro-specific syntax; works in any agent that consumes the standard.

## When to activate

Activate when the user's prompt mentions any of:

- "migrate to SageMaker", "move this to SageMaker", "run this on SageMaker"
- "convert preprocessing/training/inference to SageMaker", "use ModelTrainer", "use ModelBuilder", "use ProcessingJob"
- "SageMaker Processing job", "SageMaker training job", "SageMaker endpoint"
- "upgrade from sagemaker SDK 2.x to 3.x" / "fix v2 imports"
- A user pasting 2.x SDK code (`sagemaker.estimator.Estimator`, `XGBoost`, `SKLearnProcessor`, `Model.deploy`, `Predictor`) and asking how to update it.

The user can also invoke directly with `/sagemaker-migration`.

## When NOT to activate

- General SageMaker questions unrelated to migration (e.g., "explain SageMaker Pipelines").
- Fine-tuning of foundation models — that is the domain of the `sagemaker-ai` AWS Labs plugin (`SFTTrainer`, `DPOTrainer`, etc.), not this skill.
- Pure local ML work with no AWS surface.

## Pre-flight checks

Before generating code, verify:

1. The user has `sagemaker>=3.0` installed. If their environment has `sagemaker<3`, prompt them to upgrade (`pip install 'sagemaker>=3'`). v3 is a hard break — don't try to write code that works in both. Note `sagemaker` is a meta-package; for reproducible behaviour also pin the sub-packages (`sagemaker-core`, `sagemaker-train`, `sagemaker-serve`, `sagemaker-mlops`), which otherwise float.
2. Python 3.10+ recommended. (The pinned `sagemaker==3.12.0` wheels declare `Requires-Python >=3.9`, but the latest 3.x sub-packages have moved to `>=3.10`, so 3.10+ keeps future bumps painless.)
3. AWS credentials with `sagemaker:*`, `s3:*`, `iam:GetRole`, `iam:PassRole` for the execution role (PassRole condition often restricted to `service-role/AmazonSageMaker*`).

## Verify-before-generate rule (important)

Your training data may pre-date SDK v3. v3 reorganized class shapes, method names, and module paths — code that "looks right from memory" frequently fails. Before emitting non-trivial v3 code:

1. Cross-check imports against `references/v3-api-cheatsheet.md`.
2. For any pydantic shape (`ProcessingJob.create` arg names, `ModelTrainer.model_fields`, `InvokeEndpointOutput`), use `inspect.signature(...)` and `<Class>.model_fields` to confirm the field names live in the user's environment.
3. Use the AWS Knowledge MCP (`aws-knowledge-mcp-server`) for current docs.
4. Do NOT iterate by trial-and-error in the user's chat. Verify silently first, then emit working code.

## Hard rules — never generate v2 code

| ❌ v2 (removed) | ✅ v3 replacement |
|---|---|
| `from sagemaker.estimator import Estimator` | `from sagemaker.train import ModelTrainer` |
| `from sagemaker.xgboost import XGBoost` (and other framework subclasses) | `ModelTrainer` + `image_uris.retrieve(framework="xgboost", ...)` |
| `from sagemaker.processing import SKLearnProcessor / Processor / ScriptProcessor` | `from sagemaker.core.resources import ProcessingJob` + pydantic shapes |
| `from sagemaker.model import Model` | `from sagemaker.serve import ModelBuilder` |
| `from sagemaker.predictor import Predictor` | `model.deploy(...)` returns a v3 `Endpoint` (use `endpoint.invoke(...)`) |
| `estimator.fit({"train": "s3://..."})` | `trainer.train(input_data_config=[InputData(channel_name="train", data_source="...")])` |
| `sagemaker.__version__` | `from importlib.metadata import version; version("sagemaker")` |
| `response["Body"].read()` on endpoint invoke | `response.body.read().decode("utf-8")` (v3 returns `InvokeEndpointOutput`) |
| `processing_job.wait_for_status("Completed")` | `processing_job.wait(poll=30)` |

## Canonical v3 imports (verified against sagemaker 3.12.0)

```python
# Training
from sagemaker.train import ModelTrainer
from sagemaker.train.configs import InputData, SourceCode, Compute

# Inference / deployment
from sagemaker.serve import ModelBuilder
from sagemaker.serve.builder.schema_builder import SchemaBuilder

# Lower-level resources (Processing, Training, Endpoints) and pydantic shapes
from sagemaker.core.resources import ProcessingJob, TrainingJob, Endpoint
from sagemaker.core.shapes.shapes import (
    AppSpecification,
    ProcessingClusterConfig,
    ProcessingInput,
    ProcessingOutput,
    ProcessingOutputConfig,
    ProcessingResources,
    ProcessingS3Input,
    ProcessingS3Output,
)

# Helpers (moved in v3)
import sagemaker
from sagemaker.core.helper.session_helper import Session, get_execution_role
import sagemaker.core.image_uris as image_uris
```

`SchemaBuilder` is **not** re-exported from `sagemaker.serve` — use the deeper path.

The `sagemaker-core` PyPI distribution installs into `sagemaker/core/` — there is **no** top-level `sagemaker_core` module.

`sagemaker.train.configs` is a thin backward-compat re-export of `sagemaker.core.training.configs` and emits a one-time `DeprecationWarning` at import. Keep using `sagemaker.train.configs` — it is the path AWS's own docs use, and when `ModelTrainer` is imported first (as above) the warning fires inside library code and stays hidden under a notebook's default warning filters. If a future SDK release removes the shim, the drop-in fix is `from sagemaker.core.training.configs import InputData, SourceCode, Compute` (identical objects, no warning).

## Common patterns (project-agnostic — adapt to the user's project)

The patterns below are reusable across any SageMaker migration. They are NOT workshop-specific. If the user has project-specific conventions (e.g., custom `.env` key names, fixed S3 prefix structure), check the project's own steering / instructions first and follow those instead.

### Environment + role resolution

Use boto3-canonical env-var names in `.env` so boto3 picks them up automatically:

```python
import os, boto3
from dotenv import load_dotenv
from sagemaker.core.helper.session_helper import Session, get_execution_role

load_dotenv()
region = os.environ.get("AWS_REGION", "us-east-1")
sagemaker_session = Session(boto_session=boto3.Session(region_name=region))
try:
    role = get_execution_role()                       # works inside SageMaker
except Exception:
    role = os.environ["SAGEMAKER_EXECUTION_ROLE"]     # local fallback (use the project's role-var name)
```

Surface a clear error if a required key is missing — don't silently default to anonymous credentials.

If a project's `.env` keys mirror upstream names (e.g. CloudFormation output names) instead of boto3 canonicals, bridge them at the top of the notebook with `os.environ.setdefault(...)`. Prefer canonical names where possible — they're zero-friction for boto3.

### v3 surface validation cell

```python
from sagemaker.train import ModelTrainer
from sagemaker.core.resources import ProcessingJob
from sagemaker.serve import ModelBuilder
from importlib.metadata import version
print(f"sagemaker version: {version('sagemaker')}")
print("SDK v3 ok")
```

NOTE: never use `sagemaker.__version__` — that attribute was removed in v3.

### S3 path conventions

A pragmatic layout for end-to-end ML projects:

```
s3://<bucket>/<project>/raw/<file>.csv
s3://<bucket>/<project>/code/<script>.py
s3://<bucket>/<project>/processed/{train,validation,test,metadata}/
s3://<bucket>/<project>/training/<job-name>/output/model.tar.gz
```

If the project specifies its own prefixes (e.g., in steering), follow those instead.

### Processing job (verified shape)

See `references/v3-api-cheatsheet.md` for the full `ProcessingJob.create()` example. Key gotchas:

- Args are pydantic shapes (`ProcessingResources`, `ProcessingS3Input`, etc.), NOT v2-style nested dicts.
- Wait with `job.wait(poll=30)` — there is no `wait_for_status`.
- For SKLearn, `image_uris.retrieve(framework="sklearn", image_scope="training", ...)` — `image_scope="processing"` was removed in v3 but returns the same `sagemaker-scikit-learn` URI.

### Training job

```python
from sagemaker.train import ModelTrainer
from sagemaker.train.configs import InputData, SourceCode, Compute
import sagemaker.core.image_uris as image_uris

training_image = image_uris.retrieve(
    framework="xgboost", region=region, version="3.0-5",
)
# Use a container whose in-container XGBoost matches the local baseline (3.x). The 1.7-1 image
# writes the extensionless /opt/ml/model artifact in the LEGACY BINARY format, which local
# xgboost >= 3.1 refuses to load ("binary format ... removed in 3.1") — so any lab step that
# downloads the trained model and inspects it locally would crash. 3.0-5 saves UBJSON, which loads
# cleanly both in-container and locally. 3.0-5 is available in both the training and inference
# image scopes.
trainer = ModelTrainer(
    training_image=training_image,
    role=role,
    source_code=SourceCode(source_dir="scripts", entry_script="train.py"),
    compute=Compute(instance_type="ml.m5.xlarge", instance_count=1),
    hyperparameters={"max_depth": "5", "eta": "0.5", "num_round": "150", ...},  # all str
    base_job_name="<project-job-name>",
)
trainer.train(input_data_config=[
    InputData(channel_name="train",      data_source=train_s3),       # `data_source`, not `s3_data`
    InputData(channel_name="validation", data_source=validation_s3),
])
artifact_uri = trainer._latest_training_job.model_artifacts.s3_model_artifacts
```

### Training entry script contract (`scripts/train.py`)

- Read channel paths from env: `os.environ["SM_CHANNEL_TRAIN"]`, `os.environ["SM_CHANNEL_VALIDATION"]`.
- Save model to `/opt/ml/model/<filename>` (SageMaker tars this dir as `model.tar.gz`).
- argparse for hyperparameters; `__main__` shim; `logging` (no `print`).

### Inference entry script contract (`scripts/inference.py`)

Define the four container hooks (framework-agnostic, unchanged across v2 → v3):
- `model_fn(model_dir)` — load the model from `model_dir`.
- `input_fn(request_body, content_type)` — accept `text/csv` and `application/json`.
- `predict_fn(input_data, model)` — return predictions.
- `output_fn(prediction, accept)` — serialize as JSON or CSV.

### Inference deployment — repack workaround

`ModelBuilder` in `sagemaker==3.12.0` has a known bug when `source_code` is passed: it sets `sagemaker_session.settings._local_download_dir` to the model's S3 URI, then `_tmpdir` raises `ValueError: directory does not exist`. The robust pattern is to repack the model tar yourself and pass `s3_model_data_url`:

```python
import tarfile, tempfile, shutil, os, boto3
from urllib.parse import urlparse

# 1. Download the trained model.tar.gz
parsed = urlparse(artifact_uri)
s3 = boto3.client("s3")
with tempfile.TemporaryDirectory() as work:
    local_tar = os.path.join(work, "model.tar.gz")
    s3.download_file(parsed.netloc, parsed.path.lstrip("/"), local_tar)

    # 2. Extract, inject the inference script(s) under code/
    extract_dir = os.path.join(work, "extracted")
    os.makedirs(extract_dir)
    with tarfile.open(local_tar) as tf:
        tf.extractall(extract_dir)
    code_dir = os.path.join(extract_dir, "code")
    os.makedirs(code_dir, exist_ok=True)
    shutil.copy("scripts/inference.py", code_dir)

    # 3. Re-tar
    repacked = os.path.join(work, "repacked-model.tar.gz")
    with tarfile.open(repacked, "w:gz") as tf:
        for entry in os.listdir(extract_dir):
            tf.add(os.path.join(extract_dir, entry), arcname=entry)

    # 4. Upload as a new artifact
    repacked_key = f"{project_prefix}/training/repacked/model.tar.gz"
    s3.upload_file(repacked, bucket_name, repacked_key)
    repacked_uri = f"s3://{bucket_name}/{repacked_key}"

# 5. Hand the repacked URI to ModelBuilder — DO NOT pass source_code
from sagemaker.serve import ModelBuilder
from sagemaker.serve.builder.schema_builder import SchemaBuilder

model_builder = ModelBuilder(
    s3_model_data_url=repacked_uri,
    schema_builder=SchemaBuilder(sample_input=sample_csv, sample_output=sample_pred_csv),
    role_arn=role,
    sagemaker_session=sagemaker_session,
    image_uri=xgb_image_uri,
    content_type="text/csv",
    accept_type="application/json",
    env_vars={
      "SAGEMAKER_PROGRAM": "inference.py",                   # entry script
      "SAGEMAKER_SUBMIT_DIRECTORY": "/opt/ml/model/code",    # directory inside container where the script lives
    }
)
model_builder.build()
endpoint = model_builder.deploy(instance_type="ml.m5.xlarge", initial_instance_count=1)
```

### Endpoint invocation (smoke test)

```python
import json
response = endpoint.invoke(
    body=csv_body,                        # bytes or str
    content_type="text/csv",
    accept="application/json",
)
# `response` is InvokeEndpointOutput; `response.body` is a StreamingBody.
result = json.loads(response.body.read().decode("utf-8"))
# Built-in XGBoost container returns: {"predictions": [{"score": <float>}, ...]}
# (no `label` key) — derive the label client-side from your threshold.
```

### Endpoint cleanup

```python
endpoint.delete()  # NOT predictor.delete_endpoint() (that's v2)
```

## Failure modes to watch for

- `ModuleNotFoundError: No module named 'sagemaker.estimator'` — user is on v3 and code is v2. Rewrite using ModelTrainer.
- `cannot import name 'SchemaBuilder' from 'sagemaker.serve'` — use `from sagemaker.serve.builder.schema_builder import SchemaBuilder`.
- `cannot import name 'image_uris' from 'sagemaker'` — v3 moved it. Use `import sagemaker.core.image_uris as image_uris`.
- `cannot import name 'get_execution_role' from 'sagemaker'` — v3 moved it. Use `from sagemaker.core.helper.session_helper import Session, get_execution_role`.
- `Unsupported image scope: processing` for sklearn — v3 dropped that scope. Pass `image_scope="training"`.
- `ModuleNotFoundError: No module named 'sagemaker_core'` — user typed the package name as a module. Use `from sagemaker.core.resources import ...`.
- `AttributeError: module 'sagemaker' has no attribute '__version__'` — removed in v3. Use `importlib.metadata.version("sagemaker")`.
- `AttributeError: 'ProcessingJob' object has no attribute 'wait_for_status'` — use `.wait(poll=30)`.
- `TypeError: 'InvokeEndpointOutput' object is not subscriptable` — `Endpoint.invoke()` returns a pydantic object. Use `response.body`.
- `TypeError: the JSON object must be str, bytes or bytearray, not StreamingBody` — call `.read().decode("utf-8")` on `response.body` first.
- `KeyError: 'label'` when parsing endpoint output — built-in XGBoost container only emits `score`. Derive the label client-side from the score and threshold, or properly repack a custom `inference.py` (see deployment recipe).
- `ValueError: Inputted directory ... does not exist: 's3://...'` from `ModelBuilder.build()` — the `source_code` repack bug. Use the manual repack workaround above.
- `botocore.exceptions.ClientError: ... iam:PassRole ... is not authorized` — IAM policy's PassRole condition does not match the execution role's ARN.
- `mlflow-skinny requires starlette<1` — known transitive constraint. Accept and move on unless the user is exposing an HTTP server.
- `DeprecationWarning: sagemaker.train.configs has been moved to sagemaker.core.training.configs` — harmless re-export shim; the code is unaffected. Import `ModelTrainer` before the `configs` symbols to keep it hidden, or switch the import to `sagemaker.core.training.configs` to silence it entirely.
- `XGBoostError: ... The binary format has been deprecated in 1.6 and removed in 3.1` when loading a downloaded `/opt/ml/model/xgboost-model` locally — the training container's XGBoost (1.7) wrote the legacy binary format. Train with the `3.0-5` container image (saves UBJSON) so local `xgboost>=3.1` can load the artifact.

## Versions (current at time of writing)

The latest stable line is `sagemaker>=3.12,<4` and `sagemaker-core>=2.12,<3`. Always check `pip show sagemaker` first; if pinned to a specific minor, follow that version's release notes.

## See also

- `references/v3-api-cheatsheet.md` — short reference card for the v3 import paths and verified gotchas.
- `references/notebook-cell-format.md` — JSON cell shapes and editing rules (use when modifying `.ipynb` files).
