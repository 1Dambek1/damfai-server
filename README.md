### Репозитории проекта

- [Damfai server](https://github.com/1Dambek1/damfai-server) - backend, серверная часть
- [Damfai client](https://github.com/shms0mms/damfai-client) - frontend, визуальная часть  
# Интерфейс приложения

### И в части второго этапа мы реализовали:

- [x] Выбрать уровень сжатия текста
- [x] Суммаризировать введенный текст на
- [x] Скопировать суммаризированный текст в буфер обмена
- [x] Сжатие текста на любой из предложенных языков(английский, русский, китайский)
## Код для второго этапа на backend:

1. Подключение и скачивание модели 'utrobinmv/t5_summary_en_ru_zh_base_2048' с [Hugging Face](https://huggingface.co/) происходит в [ai_connect.py](https://github.com/1Dambek1/damfai-server/blob/main/server/src/ai_connect.py)
2. Работа и сжатие самого текста происходит в папке second_stage c файлами:
  - [second_stage_router_router](https://github.com/1Dambek1/damfai-server/blob/main/server/src/second_stage/second_stage_router.py) - функция для сжатия
  - [second_stage_router_schema](https://github.com/1Dambek1/damfai-server/blob/main/server/src/second_stage/second_stage_schema.py) - классы для типизации данных

### Код для второго этапа на tg_bot:

1. Подключение и скачивание модели 'utrobinmv/t5_summary_en_ru_zh_base_2048' с [Hugging Face](https://huggingface.co/) происходит в [ai_connect.py](https://github.com/1Dambek1/damfai-server/blob/main/server/src/second_stage/second_stage_router.py)
2. Работа и сжатие самого текста происходит в папке summarize c файлом:
  - [router](https://github.com/1Dambek1/damfai-server/blob/main/bot/src/summarize/router.py) - функция для сжатия



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

## Телеграмм Бот от damfai

##### Возможности нашего бота:

- [x] Отслеживание статистики
- [x] Детальная аналитика
- [x] Просмотр своего профиля
- [x] Озвучивание книги(Из-за недостатка токенов для озвучки текст мы решили временно отключить)
- [x] Напоминание


### Запуск серверной части

- Убедитесь, что перед этим вы запустили клиентскую часть приложения

- Для запуска вам потребуется установить Docker
  - [windows installer](https://docs.docker.com/desktop/install/windows-install/)
  - [macos installer](https://docs.docker.com/desktop/install/mac-install/)
  - [linux installer](https://docs.docker.com/desktop/install/linux/)

- Далее введите в терминал следующую команду и ждите запуска:

  docker compose up --build

- Теперь сервер запущен на http://localhost:8000/docs
- Перейдите в телеграмм и введите в поиск название бота - @damfai_bot
