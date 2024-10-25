from pydantic import BaseModel


class ShowTheme(BaseModel):
  id: int
  name: str
  description: str
  backgroundColor: str 
  textColor: str 
  primaryColor: str 
  primaryTextColor: str
  price: float | None

class CreateTheme(BaseModel):
  name: str
  description: str
  backgroundColor: str 
  textColor: str 
  primaryColor: str 
  primaryTextColor: str
  price: float | None
