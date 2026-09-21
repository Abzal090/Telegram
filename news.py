import asyncio
import html
from dataclasses import dataclass

import feedparser

NEWS_FEED_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"


@dataclass
class NewsItem:
    title: str
    link: str


async def fetch_top_news(limit: int = 10) -> list[NewsItem]:
    feed = await asyncio.to_thread(feedparser.parse, NEWS_FEED_URL)
    return [
        NewsItem(title=entry.title, link=entry.link)
        for entry in feed.entries[:limit]
    ]


def format_news_message(items: list[NewsItem]) -> str:
    if not items:
        return "Не удалось получить новости. Попробуйте позже."

    lines = ["<b>Топ новостей мира</b>\n"]
    for i, item in enumerate(items, start=1):
        title = html.escape(item.title)
        link = html.escape(item.link)
        lines.append(f'{i}. <a href="{link}">{title}</a>')
    return "\n".join(lines)
