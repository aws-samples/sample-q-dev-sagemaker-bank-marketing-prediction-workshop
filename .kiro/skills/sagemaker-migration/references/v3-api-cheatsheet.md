# SageMaker Python SDK v3 — import path cheatsheet

Verified empirically against `sagemaker==3.12.0` and `sagemaker-core==2.12.0` on 2026-05-26.

## Training

| Import | Use |
|---|---|
| `from sagemaker.train import ModelTrainer` | Replaces v2 `Estimator` and all framework subclasses (`XGBoost`, `SKLearn`, `PyTorch`, etc.). |
| `from sagemaker.train.configs import InputData` | Channel descriptor — `InputData(channel_name=..., data_source=...)`. |
| `from sagemaker.train.configs import SourceCode` | Source-code descriptor — `SourceCode(source_dir=..., entry_script=...)`. |
| `from sagemaker.train.configs import Compute` | Compute config — `Compute(instance_type=..., instance_count=...)`. |

## Inference / deployment

| Import | Use |
|---|---|
| `from sagemaker.serve import ModelBuilder` | Replaces v2 `Model`. Build → `.deploy()`. |
| `from sagemaker.serve.builder.schema_builder import SchemaBuilder` | Sample input/output schema. **Not** re-exported from `sagemaker.serve`. |

## Lower-level resources

| Import | Use |
|---|---|
| `from sagemaker.core.resources import ProcessingJob` | Replaces v2 `Processor` / `SKLearnProcessor` / `ScriptProcessor`. |
| `from sagemaker.core.resources import TrainingJob` | Lower-level training resource (use `ModelTrainer` first; `TrainingJob` for unusual configs). |

## Helpers (v2 → v3 unchanged)

| Import | Use |
|---|---|
| `import sagemaker` | Top-level convenience. |
| `from sagemaker import Session` | Session abstraction. |
| `from sagemaker import get_execution_role` | Execution role helper. |
| `import sagemaker.core.image_uris as image_uris` | `image_uris.retrieve(framework="xgboost", ...)` for built-in containers. v3 moved this module under `sagemaker.core`. |

## Removed in v3 — do not import

| Import | Why removed |
|---|---|
| `sagemaker.estimator.Estimator` | Replaced by `ModelTrainer`. |
| `sagemaker.xgboost.XGBoost` (and other framework subclasses) | Unified into `ModelTrainer` + `image_uris`. |
| `sagemaker.processing.SKLearnProcessor` (and `Processor`, `ScriptProcessor`) | Use `sagemaker.core.resources.ProcessingJob`. |
| `sagemaker.model.Model` | Use `ModelBuilder`. |
| `sagemaker.predictor.Predictor` | `model.deploy()` returns a v3 predictor. |

## Pin pattern for reproducibility

```
sagemaker==3.12.0
sagemaker-core==2.12.0   # installs into sagemaker/core/, NOT sagemaker_core
boto3==1.43.14
botocore==1.43.14
```

## Common mistakes

- `from sagemaker_core import ...` — there is no `sagemaker_core` module. Use `from sagemaker.core...`.
- `from sagemaker.serve import SchemaBuilder` — not re-exported. Use the deeper path.
- `estimator.fit({"train": "..."})` — v2 dict form. Use `InputData` list.
