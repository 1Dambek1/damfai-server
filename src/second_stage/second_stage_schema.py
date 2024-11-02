from pydantic import BaseModel
import enum

# Схема для модели ответа, определяет структуру возвращаемого JSON
class SumTextSchema(BaseModel):
    sum_text: str  # Поле для суммированного текста
    lang: str      # Поле для языка
    level: str     # Поле для уровня суммирования

# Перечисление для уровней суммирования
class LevelOfSumTextSchema(enum.Enum):
    small_sum = "summary big"     # Небольшое суммирование
    middle_sum = "summary"        # Среднее суммирование
    big_sum = "summary brief"     # Большое суммирование

# Перечисление для поддерживаемых языков
class LangOfSumTextSchema(enum.Enum):
    en = "to en"  # Английский
    ru = "to ru"  # Русский
    zh = "ro zh"  # Китайский