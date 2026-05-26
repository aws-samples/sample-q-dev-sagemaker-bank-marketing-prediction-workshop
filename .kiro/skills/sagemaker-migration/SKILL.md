---
name: sagemaker-migration
description: Migrate any local Python ML project (Jupyter notebooks, scripts, framework-agnostic) to Amazon SageMaker AI using SageMaker Python SDK v3 — covering Processing, Training, and Inference. Use when the user asks to move local ML code to SageMaker, add ModelTrainer / ModelBuilder / ProcessingJob code, or upgrade legacy SageMaker SDK 2.x code to 3.x.
license: Apache-2.0
compatibility: Requires Python 3.10+ and sagemaker>=3.0. Designed for SageMaker AI in any AWS region. No Kiro-specific syntax — runs in any agentskills.io-compatible client (Kiro IDE/CLI, Claude Code, etc.).
metadata:
  author: aws-samples
  version: "1.1.0"
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

## When NOT to activate

- General SageMaker questions unrelated to migration (e.g., "explain SageMaker Pipelines").
- Fine-tuning of foundation models — that is the domain of the `sagemaker-ai` AWS Labs plugin (`SFTTrainer`, `DPOTrainer`, etc.), not this skill.
- Pure local ML work with no AWS surface.

## Pre-flight checks

Before generating code, verify:

1. The user has `sagemaker>=3.0` installed. If their environment has `sagemaker<3`, prompt them to upgrade (`pip install 'sagemaker>=3' 'sagemaker-core>=2'`). v3 is a hard break — don't try to write code that works in both.
2. Python 3.10+ (older versions are not supported by sagemaker 3.x).
3. AWS credentials with `sagemaker:*`, `s3:*`, `iam:GetRole`, `iam:PassRole` for the execution role (PassRole condition often restricted to `service-role/AmazonSageMaker*`).

## Hard rules — never generate v2 code

The following imports raise `ModuleNotFoundError` in v3. Refuse to emit them; rewrite the request using v3 patterns.

| ❌ v2 (removed) | ✅ v3 replacement |
|---|---|
| `from sagemaker.estimator import Estimator` | `from sagemaker.train import ModelTrainer` |
| `from sagemaker.xgboost import XGBoost` (and other framework subclasses) | `ModelTrainer` + `image_uris.retrieve(framework="xgboost", ...)` |
| `from sagemaker.processing import SKLearnProcessor / Processor / ScriptProcessor` | `from sagemaker.core.resources import ProcessingJob` |
| `from sagemaker.model import Model` | `from sagemaker.serve import ModelBuilder` |
| `from sagemaker.predictor import Predictor` | `predictor = model.deploy(...)` returns a v3-compatible predictor |
| `estimator.fit({"train": "s3://..."})` | `trainer.train(input_data_config=[InputData(channel_name="train", data_source="...")])` |

## Canonical v3 imports (verified against sagemaker 3.12.0)

```python
# Training
from sagemaker.train import ModelTrainer
from sagemaker.train.configs import InputData, SourceCode, Compute

# Inference / deployment
from sagemaker.serve import ModelBuilder
from sagemaker.serve.builder.schema_builder import SchemaBuilder

# Lower-level resources (Processing)
from sagemaker.core.resources import ProcessingJob, TrainingJob

# Helpers (still in v3)
import sagemaker
from sagemaker.core.helper.session_helper import Session, get_execution_role
import sagemaker.core.image_uris as image_uris   # v3 moved image_uris under sagemaker.core
```

`SchemaBuilder` is **not** re-exported from `sagemaker.serve` — use the deeper path.

The `sagemaker-core` PyPI distribution installs into `sagemaker/core/` — there is **no** top-level `sagemaker_core` module. Use `from sagemaker.core.resources import ...`.

## Processing migration (v2 → v3)

```python
# v3
from sagemaker.core.resources import ProcessingJob
from sagemaker.core.helper.session_helper import get_execution_role
import sagemaker.core.image_uris as image_uris

# v3 NOTE: SKLearn no longer supports image_scope="processing" in v3 — use "training" (or "inference").
# Both return the same sagemaker-scikit-learn URI; v2's SKLearnProcessor used this same image.
image_uri = image_uris.retrieve(
    framework="sklearn", region="us-east-1", version="1.2-1",
    image_scope="training", instance_type="ml.m5.xlarge",
)

job = ProcessingJob.create(
    processing_job_name="my-preprocess",
    role_arn=get_execution_role(),
    app_specification={
        "ImageUri": image_uri,
        "ContainerEntrypoint": ["python3", "/opt/ml/processing/input/code/preprocessing.py"],
    },
    processing_resources={
        "ClusterConfig": {"InstanceCount": 1, "InstanceType": "ml.m5.xlarge", "VolumeSizeInGB": 30}
    },
    processing_inputs=[
        {"InputName": "raw", "S3Input": {"S3Uri": raw_s3, "LocalPath": "/opt/ml/processing/input"}},
        {"InputName": "code", "S3Input": {"S3Uri": code_s3, "LocalPath": "/opt/ml/processing/input/code"}},
    ],
    processing_output_config={"Outputs": [
        {"OutputName": "train", "S3Output": {"S3Uri": train_s3, "LocalPath": "/opt/ml/processing/output/train"}},
        {"OutputName": "validation", "S3Output": {"S3Uri": val_s3, "LocalPath": "/opt/ml/processing/output/validation"}},
        {"OutputName": "test", "S3Output": {"S3Uri": test_s3, "LocalPath": "/opt/ml/processing/output/test"}},
    ]},
)
job.wait_for_status("Completed")
```

If the user's container or configuration won't fit `ProcessingJob.create()`, fall back to `boto3.client("sagemaker").create_processing_job(...)` with the same parameter shape.

## Training migration (v2 → v3)

```python
# v3
from sagemaker.train import ModelTrainer
from sagemaker.train.configs import InputData, SourceCode, Compute
from sagemaker.core.helper.session_helper import get_execution_role
import sagemaker.core.image_uris as image_uris

trainer = ModelTrainer(
    training_image=image_uris.retrieve(framework="xgboost", region="us-east-1", version="1.7-1"),
    role=get_execution_role(),
    source_code=SourceCode(source_dir="scripts", entry_script="train.py"),
    compute=Compute(instance_type="ml.m5.xlarge", instance_count=1),
    hyperparameters={"objective": "binary:logistic", "num_round": "100", "max_depth": "5"},
    base_job_name="my-training",
)

trainer.train(input_data_config=[
    InputData(channel_name="train",      data_source=train_s3),
    InputData(channel_name="validation", data_source=validation_s3),
])
```

The user's training entry script (e.g., `scripts/train.py`) is a standalone script with a `__main__` shim that the SageMaker training container invokes. SageMaker passes hyperparameters as command-line args (`/opt/ml/input/config/hyperparameters.json`) and channels as env vars (`SM_CHANNEL_TRAIN`, etc.). Keep that contract — internal training logic does not change between SDK 2.x and 3.x.

## Inference migration (v2 → v3)

```python
# v3
from sagemaker.serve import ModelBuilder
from sagemaker.serve.builder.schema_builder import SchemaBuilder
import pandas as pd

sample_input = pd.DataFrame([{"col_a": 1.0, "col_b": "x"}])
sample_output = {"prediction": 0.0}

builder = ModelBuilder(
    model=trainer.model,
    schema_builder=SchemaBuilder(sample_input, sample_output),
    inference_spec_uri="scripts/inference.py",
    role_arn=get_execution_role(),
)

model = builder.build()
predictor = model.deploy(instance_type="ml.m5.xlarge", initial_instance_count=1)

# clean up after testing
predictor.delete_endpoint()
```

The inference entry script must define the SageMaker container hooks: `model_fn`, `input_fn`, `predict_fn`, `output_fn`. These are framework-agnostic and survive v2→v3 unchanged.

## Failure modes to watch for

- `ModuleNotFoundError: No module named 'sagemaker.estimator'` — user is on v3 and code is v2. Rewrite using ModelTrainer.
- `cannot import name 'SchemaBuilder' from 'sagemaker.serve'` — use `from sagemaker.serve.builder.schema_builder import SchemaBuilder`.
- `cannot import name 'image_uris' from 'sagemaker'` — v3 moved it. Use `import sagemaker.core.image_uris as image_uris`.
- `cannot import name 'get_execution_role' from 'sagemaker'` — v3 moved it. Use `from sagemaker.core.helper.session_helper import Session, get_execution_role`.
- `Unsupported image scope: processing` for sklearn — v3 dropped that scope. Pass `image_scope="training"` (or `"inference"`); the URI returned is the same `sagemaker-scikit-learn` container v2's `SKLearnProcessor` used.
- `ModuleNotFoundError: No module named 'sagemaker_core'` — user typed the package name as a module. Use `from sagemaker.core.resources import ...`.
- `botocore.exceptions.ClientError: ... iam:PassRole ... is not authorized` — the IAM policy's PassRole condition does not match the execution role's ARN. Either rename the role to match the condition or relax the condition.
- `mlflow-skinny requires starlette<1` — known transitive constraint. The starlette CVE only matters with an exposed HTTP server. Accept and move on unless the user is actually exposing one.

## Versions (current at time of writing — May 2026)

The latest stable line is `sagemaker>=3.12,<4` and `sagemaker-core>=2.12,<3`. Always check `pip show sagemaker` first; if pinned to a specific minor, follow that version's release notes.

## See also

- `references/v3-api-cheatsheet.md` — short reference card for the v3 import paths.
- `references/notebook-cell-format.md` — JSON cell shapes and editing rules (use when modifying `.ipynb` files).
