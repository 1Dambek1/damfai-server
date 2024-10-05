from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR  = Path(__file__).parent.parent


class AuthData(BaseModel):
    private_key :Path = BASE_DIR  / "src" / "app_auth" / "tokens" / "private_key.pem"
    
    public_key :Path = BASE_DIR  /  "src" / "app_auth"  / "tokens" / "public_key.pem"
    
    algorithm:str = "RS256"

    
    days:int = 7
    

class EnvData(BaseSettings):
    # DB_DATA
    DB_URl:str
    DB_URl_ASYNC:str
    

class EnvGigaChat(BaseSettings):
    # GIGACHAT
    AUTH_KEY_KIRIL:str
    AUTH_KEY_DENIS:str
    SCOPE:str

class TgBotEnv(BaseSettings):
    # TG_BOT
    TOKEN:str
    SITE_URL:str

class Config(BaseModel):
    
    env_data:EnvData = EnvData()
    
    gigachat_data:EnvGigaChat = EnvGigaChat()

    auth_data:AuthData = AuthData()

    
    tg_bot_data: TgBotEnv = TgBotEnv()
    
    

    
config = Config()