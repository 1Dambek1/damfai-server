from pydantic import BaseModel


class ShowExtension(BaseModel):
  id: int
  slug: str 
  description: str
  title: str

class CreateExtension(BaseModel):
  slug: str 
  description: str
  title: str
