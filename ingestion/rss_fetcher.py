#!/usr/bin/env python3
import os
import json
from datetime import datetime
from pathlib import Path
from loguru import logger
import feedparser
import newspaper
from dotenv import load_dotenv

load_dotenv()  # reads .env in working directory

FEEDS = os.getenv("RSS_FEEDS", "").split(",")
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./data/raw"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_and_store():
    for url in FEEDS:
        logger.info(f"Fetching feed: {url}")
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # limit per feed
            try:
                art = newspaper.Article(entry.link)
                art.download()
                art.parse()
                record = {
                    "title": art.title,
                    "url": entry.link,
                    "published": entry.get("published", str(datetime.utcnow())),
                    "text": art.text
                }
                # filename: sanitized title + timestamp
                fname = f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}-{abs(hash(entry.link))}.json"
                path = OUTPUT_DIR / fname
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(record, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved article to {path}")
            except Exception as e:
                logger.error(f"Error processing {entry.link}: {e}")

if __name__ == "__main__":
    fetch_and_store()
