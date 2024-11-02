from pydantic import BaseModel
from pydantic_settings import BaseSettings





class Env(BaseSettings):

	BOT_TOKEN: str
	DB_URL: str
	SITE_URL: str
	SPEECH_URL: str
	SPEECH_ACCESS_TOKEN: str


class Config(BaseModel):	
	env: Env = Env()


config = Config()