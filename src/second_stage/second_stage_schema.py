from pydantic import BaseModel

import enum

class SumTextSchema(BaseModel):
    sum_text: str
    lang: str
    level: str 
     
class LevelOfSumTextSchema(enum.Enum):
    small_sum = "summary big"
    middle_sum = "summary"
    big_sum = "summary brief"
    
class LangOfSumTextSchema(enum.Enum):
    en = "to en"
    ru = "to ru"
    zh = "ro zh"