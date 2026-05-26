---
inclusion: always
---

# SageMaker Python SDK v3 — required rules for this workshop

This workspace targets **SageMaker Python SDK v3** (`sagemaker==3.12.0`). v2 `Estimator`, `Model`, `Predictor`, and all framework subclasses (`XGBoost`, `SKLearn`, `PyTorch`, etc.) are **removed in v3** and must not be used.

For long-form examples, decision logic, and migration narrative, see the on-demand skill at `.kiro/skills/sagemaker-migration/SKILL.md`. This steering file is intentionally short — it is loaded on every chat.

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
from sagemaker.core.resources import ProcessingJob, TrainingJob

# Helpers
import sagemaker
from sagemaker.core.helper.session_helper import Session, get_execution_role
import sagemaker.core.image_uris as image_uris
```

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
- Per-lab prompt templates: `.kiro/skills/sagemaker-migration/assets/prompt-templates/`
- API cheatsheet: `.kiro/skills/sagemaker-migration/references/v3-api-cheatsheet.md`
