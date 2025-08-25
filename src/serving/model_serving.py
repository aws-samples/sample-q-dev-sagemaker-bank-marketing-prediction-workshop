"""
Model serving module for bank marketing prediction.

This module provides production-ready model serving capabilities with:
- Model loading
- Input preprocessing using in-memory transformations
- Prediction generation
- Error handling
- Logging
"""
import json
import xgboost as xgb
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoadError(Exception):
    """Raised when model artifacts cannot be loaded."""
    pass

class PreprocessingError(Exception):
    """Raised when input data preprocessing fails."""
    pass

class PredictionError(Exception):
    """Raised when model prediction fails."""
    pass

class ModelServer:
    """
    Server class for bank marketing prediction model.
    
    Handles:
    - Model loading
    - Input data preprocessing
    - Model prediction
    - Error handling and logging
    """
    
    def __init__(self, model_dir: str = "model"):
        """
        Initialize ModelServer.

        Args:
            model_dir: Directory containing model artifacts
        
        Raises:
            ModelLoadError: If model artifacts cannot be loaded
        """
        self.model_dir = Path(model_dir)
        try:
            self._load_artifacts()
            logger.info("Model server initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize model server: {str(e)}")
            raise ModelLoadError(f"Failed to load model artifacts: {str(e)}")

    def _load_artifacts(self) -> None:
        """
        Load model and metadata.
        
        Raises:
            ModelLoadError: If any artifact cannot be loaded
        """
        try:
            # Load model
            self.model = xgb.Booster()
            model_path = str(self.model_dir / "xgboost_model.json")
            self.model.load_model(model_path)
            logger.info(f"Loaded model from {model_path}")
            
            # Load metadata
            with open(self.model_dir / "model_metadata.json", 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            logger.info("Loaded model metadata")
            
        except Exception as e:
            logger.warning(f"Error loading artifacts: {str(e)}")
            raise ModelLoadError(f"Failed to load artifacts: {str(e)}")

    def _convert_feature_names(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert feature names from underscore to dot notation.
        
        Args:
            input_data: Dictionary with underscore feature names
            
        Returns:
            Dictionary with dot notation feature names
        """
        conversion_map = {
            'emp_var_rate': 'emp.var.rate',
            'cons_price_idx': 'cons.price.idx',
            'cons_conf_idx': 'cons.conf.idx',
            'nr_employed': 'nr.employed'
        }
        
        converted_data = {}
        for key, value in input_data.items():
            converted_key = conversion_map.get(key, key)
            converted_data[converted_key] = value
            
        return converted_data

    def _encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encode categorical features using the saved label mappings.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with encoded categorical features
            
        Raises:
            PreprocessingError: If encoding fails
        """
        try:
            for feature in self.metadata['categorical_features']:
                if feature in df.columns:
                    mapping = self.metadata['label_mapping'][feature]
                    if df[feature].iloc[0] not in mapping:
                        raise PreprocessingError(
                            f"Invalid value for feature '{feature}': {df[feature].iloc[0]}"
                        )
                    df[feature] = df[feature].map(mapping)
            return df
        except Exception as e:
            raise PreprocessingError(f"Failed to encode categorical features: {str(e)}")

    def _scale_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scale numeric features using the saved scaler parameters.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with scaled numeric features
            
        Raises:
            PreprocessingError: If scaling fails
        """
        try:
            numeric_features = self.metadata['numeric_features']
            mean = np.array(self.metadata['scaler_params']['mean'])
            scale = np.array(self.metadata['scaler_params']['scale'])
            
            df[numeric_features] = (df[numeric_features] - mean) / scale
            return df
        except Exception as e:
            raise PreprocessingError(f"Failed to scale numeric features: {str(e)}")

    def preprocess_input(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocess input data for prediction.
        
        Args:
            input_data: Dictionary containing feature values
            
        Returns:
            Preprocessed DataFrame ready for prediction
            
        Raises:
            PreprocessingError: If preprocessing fails
        """
        try:
            # Convert feature names from underscore to dot notation
            converted_data = self._convert_feature_names(input_data)
            
            # Convert input to DataFrame
            df = pd.DataFrame([converted_data])
            
            # Encode categorical features
            df = self._encode_categorical(df)
            
            # Scale numeric features
            df = self._scale_numeric(df)
            
            # Ensure columns are in the correct order
            df = df[self.metadata['feature_names']]
            
            logger.debug("Input preprocessing completed successfully")
            return df
            
        except Exception as e:
            logger.warning(f"Preprocessing error: {str(e)}")
            raise PreprocessingError(f"Failed to preprocess input: {str(e)}")

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction for input data.
        
        Args:
            input_data: Dictionary containing feature values
            
        Returns:
            Dictionary containing:
                - prediction: Binary prediction (0 or 1)
                - probability: Prediction probability
                - threshold: Classification threshold
                
        Raises:
            PreprocessingError: If preprocessing fails
            PredictionError: If prediction fails
        """
        try:
            # Preprocess input
            df = self.preprocess_input(input_data)
            
            # Convert to DMatrix
            dmatrix = xgb.DMatrix(df)
            
            # Get prediction probability
            pred_proba = self.model.predict(dmatrix)[0]
            
            # Convert to binary prediction using threshold
            pred_class = int(pred_proba > self.metadata['prediction_threshold'])
            
            result = {
                "prediction": pred_class,
                "probability": float(pred_proba),
                "threshold": self.metadata['prediction_threshold']
            }
            
            logger.debug(f"Prediction generated successfully: {result}")
            return result
            
        except PreprocessingError as e:
            raise e
        except Exception as e:
            logger.warning(f"Prediction error: {str(e)}")
            raise PredictionError(f"Failed to generate prediction: {str(e)}")
