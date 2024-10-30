from pydantic import BaseModel
from pydantic_settings import BaseSettings


    
class RedisSttings(BaseSettings):
        
    REDIS_DB:int
    REDIS_HOST:str
    REDIS_PORT:int
    
class CelerySttings(BaseSettings):
    

    BROKER_URL:str


class Config(BaseModel):
    
    celery:CelerySttings = CelerySttings()
    redis:RedisSttings = RedisSttings()
    
config = Config()