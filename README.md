# Bank Marketing Prediction Project

This project demonstrates a real-world machine learning workflow for predicting bank marketing campaign success, focusing on two main roles:

1. Data Scientist (DS) workflow for model development
2. Machine Learning Engineer (MLE) workflow for model deployment

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
   - Best model exported as `model/xgboost_model.json`
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

- Python 3.10+
- See requirements.txt for package dependencies

## License

This project is licensed under the MIT License - see the LICENSE file for details.
