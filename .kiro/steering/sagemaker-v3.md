---
inclusion: always
---

# SageMaker Python SDK v3 — required rules for this workshop

This workspace targets **SageMaker Python SDK v3** (`sagemaker==3.12.0`). v2 `Estimator`, `Model`, `Predictor`, and all framework subclasses (`XGBoost`, `SKLearn`, `PyTorch`, etc.) are **removed in v3** and must not be used.

For long-form examples, decision logic, and migration narrative, see the on-demand skill at `.kiro/skills/sagemaker-migration/SKILL.md`. This steering file is intentionally short — it is loaded on every chat.

## Verify before generating

The model's training data may pre-date SDK v3 — its memory of `sagemaker.<x>` import paths and method names is **not authoritative**. Before emitting any non-trivial v3 code:

1. Prefer the AWS Knowledge MCP (`aws-knowledge-mcp-server` → `search_documentation`) for current docs.
2. For exact pydantic-model field names or method signatures (`ModelTrainer`, `ModelBuilder`, `ProcessingJob`, `Endpoint`, `InvokeEndpointOutput`, etc.), inspect the installed package live before generating code that calls into it:
   ```python
   import inspect
   from sagemaker.train import ModelTrainer
   print(inspect.signature(ModelTrainer.train))
   for f in ModelTrainer.model_fields: print(f)
   ```
3. Cross-check against `.kiro/skills/sagemaker-migration/references/v3-api-cheatsheet.md` for the verified import paths.

Don't ship code "from memory" if any v2 path is involved — it almost always wastes a turn.

## Hard rules — never do these

- ❌ `from sagemaker.estimator import Estimator` — module removed in v3.
- ❌ `from sagemaker.xgboost import XGBoost` — module removed in v3.
- ❌ `from sagemaker.processing import SKLearnProcessor` (or `Processor`, `ScriptProcessor`) — module removed in v3.
- ❌ `from sagemaker.model import Model` — module removed in v3.
- ❌ `from sagemaker.predictor import Predictor` — module removed in v3.
- ❌ `from sagemaker import image_uris` — v3 moved it to `sagemaker.core.image_uris`.
- ❌ `from sagemaker import Session, get_execution_role` — v3 moved them to `sagemaker.core.helper.session_helper`.
- ❌ `from sagemaker_core.<anything>` — there is no top-level `sagemaker_core` module; the dist installs into `sagemaker.core`.
- ❌ `image_scope="processing"` for the SKLearn container — v3 dropped that scope. Use `"training"` (or `"inference"`); both return the same `sagemaker-scikit-learn` URI v2's `SKLearnProcessor` used.
- ❌ Passing input as v2-style dict `{"training": "s3://..."}` to `.fit()` — replaced by `InputData(channel_name=...)` list on `.train()`.
- ❌ `sagemaker.__version__` — attribute removed in v3. Use `from importlib.metadata import version; version("sagemaker")`.

If asked to generate v2-style code, refuse and rewrite using v3 patterns.

## Canonical v3 imports (verified against sagemaker==3.12.0)

```python
# Training
from sagemaker.train import ModelTrainer
from sagemaker.train.configs import InputData, SourceCode, Compute

# Inference / deployment
from sagemaker.serve import ModelBuilder
from sagemaker.serve.builder.schema_builder import SchemaBuilder

# Lower-level resources (Processing, etc.)
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

# Helpers
import sagemaker
from sagemaker.core.helper.session_helper import Session, get_execution_role
import sagemaker.core.image_uris as image_uris
```

## v3 surface gotchas (verified empirically — these waste a turn if you guess)

| Surface | What changed | Correct usage |
|---|---|---|
| **`sagemaker.__version__`** | Attribute removed | `from importlib.metadata import version; version("sagemaker")` |
| **`ProcessingJob.create`** | Takes pydantic shape objects, not dicts | `ProcessingResources(cluster_config=ProcessingClusterConfig(...))`, `ProcessingInput(input_name=..., s3_input=ProcessingS3Input(...))`, `ProcessingOutputConfig(outputs=[ProcessingOutput(output_name=..., s3_output=ProcessingS3Output(...))])` |
| **ProcessingJob waiter** | No `wait_for_status` | `job.wait(poll=30)` then read `processing_job_status` field |
| **`InputData` data_source** | String S3 URI | `InputData(channel_name="train", data_source="s3://bucket/prefix/")` — note `data_source`, NOT `s3_data` |
| **`ModelTrainer.train`** | Returns `None` | After `trainer.train(...)`, get the artifact via `trainer._latest_training_job.model_artifacts.s3_model_artifacts` |
| **`ModelBuilder` + `source_code`** | Triggers a repack bug in 3.12 (sets `local_download_dir` to S3 URI) | Manually inject `inference.py` into the model.tar.gz, upload as `repacked-model.tar.gz`, pass via `s3_model_data_url=...` and **omit** `source_code` |
| **`Endpoint.invoke`** | Returns `InvokeEndpointOutput` (pydantic), not a dict | `response.body.read().decode("utf-8")` — `body` is a `StreamingBody`. NOT `response["Body"]`. |
| **Built-in XGBoost container response** | Returns `{"predictions":[{"score":<float>}]}` only — no `label` field | Compute the label client-side from the score and your threshold |
| **XGBoost `model.save_model`** | UBJSON default in xgb >= 3.0 | OK, but the file has no extension — use `model.save_model("/opt/ml/model/xgboost-model")` and let xgboost guess the format on load |

## Quick migration table

| Concern | v2 (do not use) | v3 (use this) |
|---|---|---|
| Generic estimator | `from sagemaker.estimator import Estimator` | `from sagemaker.train import ModelTrainer` |
| XGBoost training | `from sagemaker.xgboost import XGBoost` | `ModelTrainer` + `image_uris.retrieve(framework="xgboost", ...)` |
| Processing | `SKLearnProcessor`, `ScriptProcessor` | `from sagemaker.core.resources import ProcessingJob` |
| Model deploy | `Model(...).deploy()` | `ModelBuilder(...).build().deploy()` |
| Input channels | `estimator.fit({"train": "s3://..."})` | `trainer.train(input_data_config=[InputData(...)])` |
| Schema declaration | implicit | `SchemaBuilder(sample_input, sample_output)` |
| `image_uris` | `from sagemaker import image_uris` | `import sagemaker.core.image_uris as image_uris` |
| Session helpers | `from sagemaker import Session, get_execution_role` | `from sagemaker.core.helper.session_helper import Session, get_execution_role` |
| Endpoint invocation | `predictor.predict(...)` | `endpoint.invoke(body=..., content_type=..., accept=...)` then `response.body.read().decode("utf-8")` |
| Version check | `sagemaker.__version__` | `from importlib.metadata import version; version("sagemaker")` |

## Notebook editing

`.ipynb` files are JSON. See `.kiro/steering/jupyter-notebook.md` (auto-loaded for `*.ipynb`).

## Pinned versions (do not auto-bump)

```
sagemaker==3.12.0
sagemaker-core==2.12.0     # installs into sagemaker/core/
boto3==1.43.14
xgboost==3.2.0
```

## When to look deeper

If the user asks for a complete code example (Processing job, ModelTrainer training, ModelBuilder deployment), refer to or load the skill:

- Skill: `.kiro/skills/sagemaker-migration/SKILL.md`
- API cheatsheet: `.kiro/skills/sagemaker-migration/references/v3-api-cheatsheet.md`
