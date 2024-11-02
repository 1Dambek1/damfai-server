from fastapi import APIRouter

from src.ai_connect import model_sum, tokenizer, device

from .second_stage_schema import SumTextSchema, LevelOfSumTextSchema, LangOfSumTextSchema

# Создаем маршрутизатор с префиксом и тегом для маршрутов
app = APIRouter(prefix="/second_stage", tags=["second_stage"])

@app.get("/sum_text", response_model=SumTextSchema)
async def sum_text(text: str, level: LevelOfSumTextSchema, lang: LangOfSumTextSchema):
    """
    Эндпоинт для суммирования текста.

    Аргументы запроса:
    - text (str): текст, который нужно суммировать.
    - level (LevelOfSumTextSchema): уровень суммирования (например, малое, среднее, большое).
    - lang (LangOfSumTextSchema): язык, на котором будет суммирование (например, английский, русский, китайский).

    Возвращает:
    - JSON с полями:
      - sum_text (str): суммированный текст.
      - lang (str): язык суммирования.
      - level (str): уровень суммирования.

    Пример запроса:
    
    Запрос:
        text = "В деревне, затерянной среди зелёных холмов, жил старик по имени Иван.
        Его жизнь протекала медленно и размеренно. Каждое утро Иван выходил на поля, чтобы заботиться о своём скромном участке земли.
        Он выращивал картофель и морковь, которые были его главным источником пищи.
        Вечера старик проводил у камина, читая книги и вспоминая молодость.
        Жизнь в деревне была тяжёлая, но Иван находил в ней простые радости."
        lang = "ru"
        level = "big_sum"
    Пример ответа:
    
    {
        "sum_text":"В деревне Ивана жил старик, который заботился о своем маленьком участке земли.",
        "lang":"ru",
        "level":"small_sum"
    }
    """
    # Формируем префикс для текста в зависимости от уровня и языка
    prefix = f"{level.value} {lang.value}:"
    src_text = prefix + text

    # Токенизируем текст с добавлением специальных символов, возвращая тензоры
    input_ids = tokenizer(src_text, return_tensors="pt")

    # Генерируем токены с помощью модели
    generated_tokens = model_sum.generate(**input_ids.to(device))

    # Декодируем результат генерации в читаемый формат
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

    # Возвращаем результат суммирования, язык и уровень
    return {"sum_text": result[0], "lang": lang.name, "level": level.name}