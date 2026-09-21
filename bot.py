import datetime
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from news import fetch_top_news, format_news_message

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я эхо-бот.\n"
        "Отправь мне любое сообщение, и я повторю его.\n"
        "Команда /help покажет список доступных команд."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/help — эта справка\n"
        "/news — топ-10 новостей мира\n\n"
        "Любое другое текстовое сообщение я просто повторю."
    )


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    items = await fetch_top_news(limit=10)
    await update.message.reply_text(
        format_news_message(items),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def send_daily_news(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.chat_id
    items = await fetch_top_news(limit=10)
    await context.bot.send_message(
        chat_id=chat_id,
        text=format_news_message(items),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def _parse_hhmm(value: str) -> tuple[int, int]:
    hour_str, minute_str = value.split(":", 1)
    return int(hour_str), int(minute_str)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN не задан. Создайте .env на основе .env.example "
            "и укажите токен, полученный от @BotFather."
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    news_chat_id = os.getenv("NEWS_CHAT_ID")
    if news_chat_id:
        hour, minute = _parse_hhmm(os.getenv("NEWS_TIME", "08:00"))
        application.job_queue.run_daily(
            send_daily_news,
            time=datetime.time(hour=hour, minute=minute, tzinfo=datetime.timezone.utc),
            chat_id=int(news_chat_id),
            name="daily_news",
        )
        logger.info(
            "Ежедневная рассылка новостей настроена на %02d:%02d UTC для чата %s",
            hour,
            minute,
            news_chat_id,
        )
    else:
        logger.info(
            "NEWS_CHAT_ID не задан — ежедневная рассылка новостей отключена. "
            "Новости всё ещё доступны по команде /news."
        )

    logger.info("Бот запущен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
