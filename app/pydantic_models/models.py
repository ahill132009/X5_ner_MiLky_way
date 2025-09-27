from typing import List, Optional, Tuple
from pydantic import BaseModel


class RequestPredict(BaseModel):
    input: str

class NerEntity(BaseModel):
    entity: Tuple[int, int, str]

class Entities(BaseModel):
    entities: List[Optional[Tuple[int, int, str]]]