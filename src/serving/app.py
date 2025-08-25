"""
FastAPI application for serving bank marketing predictions.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from .model_serving import ModelServer

# Initialize FastAPI app
app = FastAPI(
    title="Bank Marketing Prediction API",
    description="API for predicting bank marketing campaign success",
    version="1.0.0"
)

# Initialize model server
model_server = ModelServer()

class JobType(str, Enum):
    admin = "admin"
    blue_collar = "blue-collar"
    entrepreneur = "entrepreneur"
    housemaid = "housemaid"
    management = "management"
    retired = "retired"
    self_employed = "self-employed"
    services = "services"
    student = "student"
    technician = "technician"
    unemployed = "unemployed"
    unknown = "unknown"

class MaritalStatus(str, Enum):
    divorced = "divorced"
    married = "married"
    single = "single"
    unknown = "unknown"

class Education(str, Enum):
    basic_4y = "basic.4y"
    basic_6y = "basic.6y"
    basic_9y = "basic.9y"
    high_school = "high.school"
    illiterate = "illiterate"
    professional_course = "professional.course"
    university_degree = "university.degree"
    unknown = "unknown"

class Month(str, Enum):
    jan = "jan"
    feb = "feb"
    mar = "mar"
    apr = "apr"
    may = "may"
    jun = "jun"
    jul = "jul"
    aug = "aug"
    sep = "sep"
    oct = "oct"
    nov = "nov"
    dec = "dec"

class DayOfWeek(str, Enum):
    mon = "mon"
    tue = "tue"
    wed = "wed"
    thu = "thu"
    fri = "fri"

class Contact(str, Enum):
    cellular = "cellular"
    telephone = "telephone"

class POutcome(str, Enum):
    failure = "failure"
    nonexistent = "nonexistent"
    success = "success"

class YesNo(str, Enum):
    yes = "yes"
    no = "no"
    unknown = "unknown"

class PredictionRequest(BaseModel):
    # Personal Information
    age: int = Field(..., description="Age of the client", ge=18, le=100)
    job: JobType = Field(..., description="Type of job")
    marital: MaritalStatus = Field(..., description="Marital status")
    education: Education = Field(..., description="Education level")
    
    # Financial Information
    default: YesNo = Field(..., description="Has credit in default?")
    housing: YesNo = Field(..., description="Has housing loan?")
    loan: YesNo = Field(..., description="Has personal loan?")
    
    # Campaign Information
    contact: Contact = Field(..., description="Contact communication type")
    month: Month = Field(..., description="Last contact month of year")
    day_of_week: DayOfWeek = Field(..., description="Last contact day of the week")
    duration: int = Field(..., description="Last contact duration in seconds", ge=0)
    campaign: int = Field(..., description="Number of contacts performed during this campaign for this client", ge=1)
    pdays: int = Field(..., description="Number of days that passed by after the client was last contacted (-1 means client was not previously contacted)")
    previous: int = Field(..., description="Number of contacts performed before this campaign for this client", ge=0)
    poutcome: POutcome = Field(..., description="Outcome of the previous marketing campaign")
    
    # Economic Indicators
    emp_var_rate: float = Field(..., description="Employment variation rate - quarterly indicator")
    cons_price_idx: float = Field(..., description="Consumer price index - monthly indicator")
    cons_conf_idx: float = Field(..., description="Consumer confidence index - monthly indicator")
    euribor3m: float = Field(..., description="Euribor 3 month rate - daily indicator")
    nr_employed: float = Field(..., description="Number of employees - quarterly indicator")

    class Config:
        schema_extra = {
            "example": {
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
            }
        }

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="Binary prediction (1: will subscribe, 0: will not subscribe)")
    probability: float = Field(..., description="Probability of subscribing to the term deposit")
    threshold: float = Field(..., description="Probability threshold used for binary prediction")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make a prediction for bank marketing campaign success.
    
    Returns:
    - prediction: Binary prediction (1: will subscribe, 0: will not subscribe)
    - probability: Probability of subscribing to the term deposit
    - threshold: Probability threshold used for binary prediction
    """
    try:
        # Convert Pydantic model to dict
        input_data = request.dict()
        
        # Get prediction from model server
        result = model_server.predict(input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Check if the service is healthy."""
    return {"status": "healthy"}
