from pydantic import BaseModel

from server.src.books.books_models import EmoteEnum

class SaveEmoteEnum(BaseModel):	
	emote: EmoteEnum