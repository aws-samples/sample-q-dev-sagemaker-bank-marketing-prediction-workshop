# SageMaker Python SDK v3 — import path cheatsheet

Verified empirically against `sagemaker==3.12.0` and `sagemaker-core==2.12.0`.

## Training

| Import | Use |
|---|---|
| `from sagemaker.train import ModelTrainer` | Replaces v2 `Estimator` and all framework subclasses (`XGBoost`, `SKLearn`, `PyTorch`, etc.). |
| `from sagemaker.train.configs import InputData` | Channel descriptor — `InputData(channel_name=..., data_source=...)`. The argument is `data_source` (string S3 URI), NOT `s3_data`. |
| `from sagemaker.train.configs import SourceCode` | Source-code descriptor — `SourceCode(source_dir=..., entry_script=...)`. |
| `from sagemaker.train.configs import Compute` | Compute config — `Compute(instance_type=..., instance_count=...)`. |

After `trainer.train(...)` (returns `None`), retrieve artifacts:
```python
artifact_uri = trainer._latest_training_job.model_artifacts.s3_model_artifacts
```

## Inference / deployment

| Import | Use |
|---|---|
| `from sagemaker.serve import ModelBuilder` | Replaces v2 `Model`. Build → `.deploy()`. |
| `from sagemaker.serve.builder.schema_builder import SchemaBuilder` | Sample input/output schema. **Not** re-exported from `sagemaker.serve`. |

`ModelBuilder` + `source_code` repack bug in 3.12 — see "Common mistakes" below for the workaround.

`ModelBuilder.deploy(...)` returns a `sagemaker.core.resources.Endpoint`. Invoke with:
```python
response = endpoint.invoke(body=csv_str, content_type="text/csv", accept="application/json")
result = json.loads(response.body.read().decode("utf-8"))
```
`response.body` is a `botocore.response.StreamingBody` — `.read().decode(...)` it before parsing.

## Lower-level resources

| Import | Use |
|---|---|
| `from sagemaker.core.resources import ProcessingJob` | Replaces v2 `Processor` / `SKLearnProcessor` / `ScriptProcessor`. |
| `from sagemaker.core.resources import TrainingJob` | Lower-level training resource (use `ModelTrainer` first; `TrainingJob` for unusual configs). |
| `from sagemaker.core.resources import Endpoint` | What `ModelBuilder.deploy()` returns. Methods: `invoke`, `delete`. |

`ProcessingJob.create(...)` takes pydantic shapes, not v2-style dicts:

```python
from sagemaker.core.shapes.shapes import (
    AppSpecification, ProcessingClusterConfig, ProcessingInput, ProcessingOutput,
    ProcessingOutputConfig, ProcessingResources, ProcessingS3Input, ProcessingS3Output,
)

job = ProcessingJob.create(
    processing_job_name="my-preprocess",
    role_arn=role,
    app_specification=AppSpecification(
        image_uri=sklearn_image_uri,
        container_entrypoint=["python3", "/opt/ml/processing/input/code/preprocessing.py"],
    ),
    processing_resources=ProcessingResources(
        cluster_config=ProcessingClusterConfig(
            instance_count=1, instance_type="ml.m5.xlarge", volume_size_in_gb=30,
        ),
    ),
    processing_inputs=[
        ProcessingInput(
            input_name="raw",
            s3_input=ProcessingS3Input(
                s3_uri=raw_s3, local_path="/opt/ml/processing/input",
                s3_data_type="S3Prefix", s3_input_mode="File",
            ),
        ),
        ProcessingInput(
            input_name="code",
            s3_input=ProcessingS3Input(
                s3_uri=code_s3, local_path="/opt/ml/processing/input/code",
                s3_data_type="S3Prefix", s3_input_mode="File",
            ),
        ),
    ],
    processing_output_config=ProcessingOutputConfig(outputs=[
        ProcessingOutput(
            output_name="train",
            s3_output=ProcessingS3Output(
                s3_uri=train_s3, local_path="/opt/ml/processing/output/train",
                s3_upload_mode="EndOfJob",
            ),
        ),
        # … validation, test, metadata
    ]),
)
job.wait(poll=30)   # NOT wait_for_status
```

## Helpers (moved in v3)

| Import | Use |
|---|---|
| `import sagemaker` | Top-level convenience. |
| `from sagemaker.core.helper.session_helper import Session, get_execution_role` | Moved from top-level in v3. |
| `import sagemaker.core.image_uris as image_uris` | `image_uris.retrieve(framework="xgboost", ...)` for built-in containers. |
| `from importlib.metadata import version` | `version("sagemaker")` — `sagemaker.__version__` was removed in v3. |

## Removed in v3 — do not import

| Import | Why removed |
|---|---|
| `sagemaker.estimator.Estimator` | Replaced by `ModelTrainer`. |
| `sagemaker.xgboost.XGBoost` (and other framework subclasses) | Unified into `ModelTrainer` + `image_uris`. |
| `sagemaker.processing.SKLearnProcessor` (and `Processor`, `ScriptProcessor`) | Use `sagemaker.core.resources.ProcessingJob`. |
| `sagemaker.model.Model` | Use `ModelBuilder`. |
| `sagemaker.predictor.Predictor` | `model.deploy()` returns a v3 `Endpoint`. |

## Pin pattern for reproducibility

```
sagemaker==3.12.0
sagemaker-core==2.12.0   # installs into sagemaker/core/, NOT sagemaker_core
boto3==1.43.14
botocore==1.43.14
```

## Common mistakes (these waste turns — don't guess)

- `from sagemaker_core import ...` — there is no `sagemaker_core` module. Use `from sagemaker.core...`.
- `from sagemaker.serve import SchemaBuilder` — not re-exported. Use the deeper path.
- `estimator.fit({"train": "..."})` — v2 dict form. Use `InputData` list.
- `sagemaker.__version__` — attribute removed in v3. Use `importlib.metadata.version("sagemaker")`.
- `processing_job.wait_for_status("Completed")` — there is only `.wait(poll=...)`; the status is on `processing_job.processing_job_status` after polling.
- `response["Body"].read()` on `endpoint.invoke()` — that is the v2 boto3 raw shape. v3 returns `InvokeEndpointOutput` with attributes — use `response.body.read().decode("utf-8")`.
- `ModelBuilder(model=trainer, source_code=SourceCode(...))` — broken in 3.12: it sets `sagemaker_session.settings._local_download_dir` to the model's S3 URI, then `_tmpdir` raises `ValueError: directory does not exist`. **Workaround:** download the trained `model.tar.gz`, inject `inference.py` (and any sibling scripts) under a top-level `code/` directory inside the tar, re-upload as `repacked-model.tar.gz`, then call `ModelBuilder(s3_model_data_url=repacked_uri, schema_builder=..., role_arn=..., image_uri=...)` — **omit `source_code`**.
- The built-in XGBoost serving container only emits `{"predictions": [{"score": <float>}]}` — there is no `label` key. If your inference script defines `output_fn` to add a label, that script only takes effect if it's properly packaged into the model tarball under `code/` (see the repack workaround). If you can't repack, derive the label on the client from the score and your threshold.
