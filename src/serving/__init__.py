"""
Bank Marketing Prediction Model Serving Package
"""
from .model_serving import ModelServer
from .app import app

__all__ = ['ModelServer', 'app']
