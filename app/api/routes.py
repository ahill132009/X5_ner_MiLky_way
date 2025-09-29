from fastapi import APIRouter, HTTPException, Request
from pydantic_models.models import RequestPredict
from model_processing.ner import Predictor
from config import settings
import time
# from typing import List, Optional, Tuple

router = APIRouter(prefix="/api", tags=["NER"])

@router.post("/predict")
async def predict_ner(payload: RequestPredict, request: Request):
    try:
        if payload.input == "":
            return []
        a = time.time()
        loaded_model = request.app.state.loaded_model
        predictor = Predictor(loaded_model[0], loaded_model[1])
        entities = predictor.predict_all_entities(payload.input)
        print(entities)
        b = time.time()
        print(f'took {b-a} sec')
        # time.sleep(10)
        return entities
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")