# Telegram Bot

Telegram-бот на Python ([python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)), который отвечает на команды `/start`, `/help`, `/news` (топ-10 новостей мира) и повторяет («эхо») любое текстовое сообщение. Также умеет автоматически присылать топ-10 новостей раз в день по расписанию.

## Установка

1. Создайте виртуальное окружение и установите зависимости:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Получите токен бота у [@BotFather](https://t.me/BotFather):
   - Отправьте `/newbot`
   - Следуйте инструкциям и скопируйте выданный токен

3. Скопируйте `.env.example` в `.env` и вставьте токен:

   ```bash
   cp .env.example .env
   ```

   ```
   TELEGRAM_BOT_TOKEN=ваш-токен
   ```

4. (Опционально) Чтобы бот сам, раз в день, присылал топ-10 новостей мира в конкретный чат — укажите в `.env`:

   ```
   NEWS_CHAT_ID=ваш-chat-id
   NEWS_TIME=08:00
   ```

   Свой `chat_id` можно узнать, написав боту [@userinfobot](https://t.me/userinfobot). `NEWS_TIME` — время в UTC, по умолчанию `08:00`. Если `NEWS_CHAT_ID` не задан, автоматическая рассылка отключена, но команда `/news` всё равно работает по запросу.

## Запуск

```bash
python bot.py
```

Бот запустится в режиме polling и будет отвечать в Telegram.

## Команды

- `/start` — приветствие
- `/help` — список команд
- `/news` — топ-10 новостей мира по запросу (источник: BBC World RSS)
- любое текстовое сообщение — бот повторит его в ответ

## Источник новостей

Новости берутся из бесплатной RSS-ленты BBC World (`http://feeds.bbci.co.uk/news/world/rss.xml`), API-ключ не требуется. Логика получения и форматирования новостей — в `news.py`.
