> Please refer to the following resources for the self-service workshop content:
> - [AWS Workshop Content Manifest](https://catalog.us-east-1.prod.workshops.aws/workshops/be5424c9-7f99-4311-8294-d199a9d485c7/en-US)

# Bank Marketing Prediction Project

This project demonstrates a real-world machine learning workflow for predicting bank marketing campaign success, with both a **local baseline** ("before") and a **SageMaker AI v3** migration ("after"):

- **Data Scientist (DS) baseline** — local Jupyter + scikit-learn + XGBoost (`notebooks/model_development.ipynb`)
- **MLE baseline** — local FastAPI serving (`src/serving/`)
- **SageMaker v3 migration** — `notebooks/model_development_sagemaker.ipynb` plus `scripts/{preprocessing,train,inference}.py`, using `sagemaker.train.ModelTrainer`, `sagemaker.serve.ModelBuilder`, and `sagemaker.core.resources.ProcessingJob`

The migration is taught through the [companion workshop walkthrough](https://catalog.us-east-1.prod.workshops.aws/workshops/be5424c9-7f99-4311-8294-d199a9d485c7/en-US) using **Kiro**. The Kiro IDE chat panel is the recommended surface; the Kiro CLI is the terminal-only fallback (e.g. for the Workshop Studio code-server). Every prompt in the walkthrough is presented with two tabs (IDE / CLI) — prefer the IDE where you can install it.

## Workshop context (`.kiro/`)

This repo ships with the context Kiro auto-loads from `.kiro/`:

- `.kiro/steering/sagemaker-v3.md` — SageMaker SDK v3 rules and import patterns (always-on)
- `.kiro/steering/jupyter-notebook.md` — notebook editing rules (active on `*.ipynb`)
- `.kiro/steering/migration-rules.md` — workshop-specific do/don'ts (always-on)
- `.kiro/skills/sagemaker-migration/` — portable [agentskills.io](https://agentskills.io) skill (works in Claude Code, Kiro, or any agentskills-compatible client)
- `.kiro/skills/aws-drawio-diagram/` — AWS architecture diagram skill (uses the `@drawio` MCP)
- `.kiro/settings/mcp.json` — MCP bundle (AWS docs, AWS API read-only, drawio)

When you open this folder in Kiro IDE or run `kiro-cli chat` from the repo root, Kiro's default agent picks up steering, skills, and MCP servers automatically. To verify, run `/context show` and `/mcp` in chat.

## Data Science Workflow

The Data Science workflow is documented in `notebooks/model_development.ipynb` and includes:

1. Data Collection & Loading
   - Automatic dataset download if not present
   - Data validation and initial inspection

2. Exploratory Data Analysis (EDA)
   - Data quality assessment
   - Feature distributions
   - Target analysis
   - Feature relationships

3. Data Preprocessing
   - Target encoding
   - Categorical feature encoding
   - Numeric feature scaling
   - Train/validation/test splitting

4. Model Development & Training
   - Cross-validation training
   - Hyperparameter tuning using GridSearchCV
   - Final model training with best parameters

5. Model Evaluation
   - ROC-AUC score
   - Confusion matrix
   - Feature importance analysis
   - Precision-Recall curves

6. Model Export
   - Model saving
   - Metadata export with preprocessing parameters

### Getting Started with DS Workflow

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch Jupyter:
```bash
jupyter notebook
```

4. Open `notebooks/model_development.ipynb` to start the DS workflow
   - By running the notebook, you will:
     - Download the dataset if not present
   - All preprocessing steps are performed in-memory

## Machine Learning Engineering Workflow

The MLE workflow focuses on deploying and serving the model in production. The workflow integrates with MLflow for model tracking and versioning:

1. Model Artifact Management
   - Best model exported as `model/xgboost-model`
   - Model metadata stored in `model/model_metadata.json`:
     - Feature names and types
     - Label mappings for categorical features
     - Scaling parameters for numeric features
     - Model hyperparameters
     - Performance metrics

2. Model Serving API
   - FastAPI-based REST API
   - In-memory preprocessing pipeline
     - No dependency on serialized preprocessing objects
     - Stateless transformation using stored parameters
   - Input validation with Pydantic
   - Comprehensive error handling
   - Logging system

### Starting the Model Serving API

1. Ensure virtual environment is activated and dependencies are installed

2. Run the API:
```bash
python scripts/run_api.py
```

3. API will be available at `http://localhost:8000`

### API Endpoints

- `POST /predict`
  - Accepts JSON payload with feature values
  - Returns prediction probability and binary prediction
  - Example:
    ```bash
    curl -X POST "http://localhost:8000/predict" \
         -H "Content-Type: application/json" \
         -d '{
             "age": 41,
             "job": "management",
             "marital": "married",
             "education": "university.degree",
             "default": "no",
             "housing": "yes",
             "loan": "no",
             "contact": "cellular",
             "month": "may",
             "day_of_week": "mon",
             "duration": 240,
             "campaign": 1,
             "pdays": -1,
             "previous": 0,
             "poutcome": "nonexistent",
             "emp_var_rate": 1.1,
             "cons_price_idx": 93.994,
             "cons_conf_idx": -36.4,
             "euribor3m": 4.857,
             "nr_employed": 5191.0
         }'
    ```

## Requirements

- **Python 3.10 and above** (workshop is built and tested against 3.12)
- AWS credentials with `sagemaker:*`, `s3:*`, `iam:GetRole`, `iam:PassRole` (the SageMaker labs run real Processing/Training/Endpoint jobs)
- Pinned dependency set — see `requirements.txt`. Highlights:
  - `sagemaker==3.12.0`, `sagemaker-core==2.12.0` (SDK v3)
  - `boto3==1.43.14`
  - `xgboost==3.2.0`, `scikit-learn==1.5.2`, `pandas==2.2.3`
  - `jupyterlab==4.5.7`, `python-dotenv==1.2.2`, `uv==0.11.6`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
