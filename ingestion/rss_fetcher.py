#!/usr/bin/env python3
import os, json
from datetime import datetime
from loguru import logger
import feedparser
import newspaper
from dotenv import load_dotenv
from pymongo import MongoClient, errors

# ─── Logging ─────────────────────────────────────────────────────
logger.remove()
logger.add(lambda m: print(m, end=""), level="DEBUG")

# ─── Load Config ─────────────────────────────────────────────────
load_dotenv()

FEEDS = [u.strip() for u in os.getenv("RSS_FEEDS", "").split(",") if u.strip()]
DB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "tyche")
COLL_NAME = os.getenv("MONGO_COLLECTION", "articles")

# ─── Setup MongoDB Client ────────────────────────────────────────
client = MongoClient(DB_URI)
db = client[DB_NAME]
collection = db[COLL_NAME]

# Create a unique index on URL to prevent duplicates
try:
    collection.create_index("url", unique=True)
    logger.debug("Ensured unique index on 'url'")
except errors.DuplicateKeyError:
    pass

# ─── Core Fetch & Store ─────────────────────────────────────────
def fetch_and_store(limit_per_feed: int = 5):
    logger.info(f"Starting fetch_and_store(limit_per_feed={limit_per_feed})")
    for feed_url in FEEDS:
        logger.info(f"Parsing RSS feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            logger.warning(f"No entries for {feed_url}")
            continue

        for entry in feed.entries[:limit_per_feed]:
            link = entry.get("link")
            pub = entry.get("published", datetime.utcnow().isoformat())
            logger.debug(f"Processing: {link}")

            try:
                article = newspaper.Article(link)
                article.download()
                article.parse()

                doc = {
                    "title": article.title,
                    "url": link,
                    "published": pub,
                    "fetched_at": datetime.utcnow(),
                    "text": article.text
                }

                # Upsert into Mongo: insert if new, skip if exists
                res = collection.update_one(
                    {"url": link},
                    {"$setOnInsert": doc},
                    upsert=True
                )
                if res.upserted_id:
                    logger.success(f"Inserted new article: {link}")
                else:
                    logger.info(f"Skipping duplicate: {link}")

            except Exception as e:
                logger.error(f"Error with {link}: {e}")

if __name__ == "__main__":
    fetch_and_store(limit_per_feed=5)
    client.close()
