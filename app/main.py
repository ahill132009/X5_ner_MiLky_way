import re
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sys


app = FastAPI(title="NER Hackathon Stub (Async, rule-based)")

class PredictIn(BaseModel):
    input: str

class SpanOut(BaseModel):
    start_index: int
    end_index: int
    entity: str

CYRILLIC_RE = re.compile(r'^[А-Яа-яЁё]', re.UNICODE)
LATIN_RE = re.compile(r'^[A-Za-z]')
DIGIT_RE = re.compile(r'^\d')
TOKEN_RE = re.compile(r'\S+')

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/predict", response_model=List[SpanOut])
async def predict(payload: PredictIn) -> List[SpanOut]:
    text = payload.input
    if text == "":
        return []

    spans: List[SpanOut] = []
    prev_type: str | None = None

    for m in TOKEN_RE.finditer(text):
        token = m.group(0)
        start = m.start()
        end = m.end()

        if CYRILLIC_RE.match(token):
            typ = "TYPE"
        elif LATIN_RE.match(token):
            typ = "BRAND"
        elif DIGIT_RE.match(token):
            typ = "VOLUME"
        else:
            prev_type = None
            continue

        prefix = "I-" if prev_type == typ else "B-"
        entity = f"{prefix}{typ}"

        spans.append(SpanOut(start_index=start, end_index=end, entity=entity))
        prev_type = typ

    return spans