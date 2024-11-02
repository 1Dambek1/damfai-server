from pydantic import BaseModel


class ShowExtension(BaseModel):
  id: int
  slug: str 
  description: str
  title: str

