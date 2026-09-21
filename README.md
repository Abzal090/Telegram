# Telegram Echo Bot

Простой Telegram-бот на Python ([python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)), который отвечает на команды `/start`, `/help` и повторяет («эхо») любое текстовое сообщение.

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

## Запуск

```bash
python bot.py
```

Бот запустится в режиме polling и будет отвечать в Telegram.

## Команды

- `/start` — приветствие
- `/help` — список команд
- любое текстовое сообщение — бот повторит его в ответ
