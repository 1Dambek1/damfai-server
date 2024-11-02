  
### Репозитории проекта


- [Damfai server](https://github.com/1Dambek1/damfai-server) - backend, серверная часть

- [Damfai client](https://github.com/shms0mms/damfai-client) - frontend, визуальная часть

- [Damfai telegram bot](https://github.com/shms0mms/damfai-bot) - tg bot

  
# Интерфейс приложения

### И в части второго этапа мы реализовали:

  
- [x] Выбрать уровень сжатия текста
- [x] Суммаризировать введенный текст на
- [x] Скопировать суммаризированный текст в буфер обмена
- [x] Сжатие текста на любой из предложенных языков(английский, русский, китайский)

### Код для второго этапа:

1. Подключение и скачивание модели 'utrobinmv/t5_summary_en_ru_zh_base_2048' с [Hugging Face](https://huggingface.co/) происходит в [ai_connect.py](https://github.com/1Dambek1/damfai-server/blob/main/src/ai_connect.py)
2. Работа и сжатие самого текста происходит в папке second_stage c файлами:
	- [second_stage_router_router](https://github.com/1Dambek1/damfai-server/blob/main/src/second_stage/second_stage_router.py) - функция для сжатия
	- [second_stage_router_schema](https://github.com/1Dambek1/damfai-server/blob/main/src/second_stage/second_stage_schema.py) - классы для типизации данных



### Мы создали сервис damfai, где в основном интерфейсе можно:


- [x] Создавать аккаунт
- [x] Смотреть аналитику и статистику чтения
- [x] Учавствовать в гонках по чтению книг
- [x] Свободно читать любые книги
- [ ] Читать книги, сжатые под ваши потребности
- [x] Поиск книг
- [x] Умная система рекомендаций
- [x] Подборка книг по вашему настроению
- [x] Задавать вопросы при чтении у AI-ассистента Чаппи
- [ ] проходить чаппи-пасс или же дорогу чаппи, выполняя квесты
- [ ] Покупать мерч за чаппи коины
- [x] Озвучка текста в телеграмм боте


### Запуск серверной части

- Убедитесь, что перед этим вы запустили клиентскую часть приложения

- Для запуска вам потребуется установить Docker
	- [windows installer](https://docs.docker.com/desktop/install/windows-install/)
	- [macos installer](https://docs.docker.com/desktop/install/mac-install/)
	- [linux installer](https://docs.docker.com/desktop/install/linux/)

- Далее введите в терминал следующую команду и ждите запуска:

```bash
	docker compose up --build
```

  
- Теперь сервер запущен на http://localhost:8000

