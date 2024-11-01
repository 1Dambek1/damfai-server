from pydantic import BaseModel
from typing import Optional

import enum

class SumTextSchema(BaseModel):
    sum_text: str
    lang: str = "ru"
    level: str = "easy"
    
    
class LevelOfSumTextSchema(enum.Enum):
    small_sum = "summary big"
    middle_sum = "summary"
    big_sum = "summary brief"
    
class LangOfSumTextSchema(enum.Enum):
    en = "to en"
    ru = "to ru"
    zh = "ro zh"