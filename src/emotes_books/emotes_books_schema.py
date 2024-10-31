
from pydantic import BaseModel
from ..books.books_models import EmoteEnum
class SaveEmoteEnum(BaseModel):	
	emote: EmoteEnum