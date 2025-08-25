# Migrating Bank Marketing Prediction to Amazon SageMaker

This document outlines the process of migrating the existing bank marketing prediction workflow to Amazon SageMaker. The migration will transform the current local setup (Jupyter Notebook for preprocessing/training and Flask API for deployment) to a SageMaker-based workflow.

## Current vs. Target Setup

**Current Setup:**
- Preprocessing and model training in local Jupyter Notebook
- Model deployment via local FastAPI service

**Target Setup:**
- Local development environment with SageMaker SDK
- SageMaker Processing Jobs for data preprocessing
- SageMaker Training Jobs for model training
- SageMaker Endpoints for model deployment

## Migration Roadmap

1. Initial Setup and Environment Configuration
2. Data Preparation for SageMaker
3. Converting Preprocessing to SageMaker Processing
4. Converting Model Training to SageMaker Training
5. Model Deployment with SageMaker Endpoint
6. Preprocessing Testing Framework

## Project Directory Structure

```
bank-marketing-prediction/
│
├── data/
│   ├── raw/                      # Raw dataset files
│   └── processed/                # Processed datasets (local copies)
│       └── preprocess_metadata.json       # Preprocessing metadata
│
├── model/
│   ├── model_metadata.json       # Model metadata and parameters
│   └── xgboost-model             # Local copy of trained model
│
├── notebooks/
│   ├── model_development.ipynb           # Original local workflow notebook
│   └── model_development_sagemaker.ipynb # New SageMaker workflow notebook
│
├── scripts/
│   ├── preprocess.py         # SageMaker Preprocessing script
│   ├── train.py              # SageMaker Training script
│   ├── inference.py          # SageMaker inference script
│   └── run_api.py            # Original FastAPI server script
│
├── src/
│   └── processed/                 # Processed datasets (local copies)
│       ├── app.py                 # Originial FastAPI server app
│       └── model_serving.py       # Original model serving module
│
├── tests/
│   └── test_preprocess.py
│
├── requirements.txt              # Project dependencies
├── JUPYTER_NOTEBOOK_FORMAT.md    # Jupyter Notebook structure and guidelines
├── README.md                     # Original project documentation
└── SAGEMAKER_MIGRATION.md        # This migration guide
```