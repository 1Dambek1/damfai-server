from pydantic import BaseModel

from src.books.books_models import EmoteEnum

class SaveEmoteEnum(BaseModel):	
	emote: EmoteEnum