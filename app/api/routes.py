from fastapi import APIRouter, HTTPException, Request
from pydantic_models.models import RequestPredict, Entities
from model_processing.ner import Predictor
from config import settings

router = APIRouter(prefix="/api", tags=["NER"])

@router.post("/predict", response_model=Entities)
async def predict_ner(payload: RequestPredict, request: Request):
    try:
        loaded_model = request.app.state.loaded_model
        predictor = Predictor(loaded_model[0], loaded_model[1])
        entities = predictor.predict_all_entities(payload.input)
        print(entities)
        return Entities(entities=entities)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")