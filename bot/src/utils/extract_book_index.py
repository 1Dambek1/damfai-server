def extract_book_index(book_string: str) -> int:
    """
    Извлекает индекс книги из строки формата "индекс. название".
    
    :param book_string: Строка, содержащая индекс и название книги.
    :return: Индекс книги как целое число.
    """
    try:
        index_str = book_string.split('.')[0].strip()  # Получаем часть до точки и убираем лишние пробелы
        index = int(index_str)  # Преобразуем в целое число
        return index
    except (ValueError, IndexError):
        raise ValueError("Некорректный формат строки. Убедитесь, что строка имеет формат 'индекс. название'.")

