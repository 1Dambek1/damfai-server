from pydantic import BaseModel


class ShowTheme(BaseModel):
  id: int
  name: str
  description: str
  light: dict
  dark: dict
  price: float | None
  key: str

class CreateTheme(BaseModel):
  name: str
  description: str
  light: dict
  dark: dict
  price: float | None
  key: str
