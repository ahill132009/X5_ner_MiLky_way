from fastapi import APIRouter, HTTPException, Request
from pydantic_models.models import RequestPredict
from config import settings
import time
import asyncio
from logger import logger
from concurrent.futures import ThreadPoolExecutor
from model_processing.postprocess import process_entities

# from typing import List, Optional, Tuple

router = APIRouter(prefix="/api", tags=["NER"])

executor = ThreadPoolExecutor(max_workers=1)

@router.post("/predict")
async def predict_ner(payload: RequestPredict, request: Request, _logger=logger):
    try:
        if payload.input == "":
            return []
        start = time.perf_counter()
        _logger.debug(f"use cuda: {settings.use_cuda}")
        if settings.use_cuda:
            predictor = request.app.state.predictor
            entities = predictor.predict_all_entities(payload.input)
        else:
            loop = asyncio.get_event_loop()
            predictor = request.app.state.predictor
            entities = await loop.run_in_executor(
                executor,
                predictor.predict_all_entities,
                payload.input
        )
        latency = time.perf_counter() - start
        _logger.info(f'Prediction took: {latency:.4f}s | Entities: {entities}')
        # time.sleep(10)
        processed_entities = process_entities(entities)
        return processed_entities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")