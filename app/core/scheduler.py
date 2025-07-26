from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.rss import scrape_hacker_news, scrape_techcrunch, scrape_reddit
from app.core.email import send_email_digest
import logging

logger = logging.getLogger(__name__)

def start_scheduler():

    scheduler = AsyncIOScheduler(timezone="UTC")

    scheduler.add_job(
        func=lambda: _run_scrapers(),
        trigger=CronTrigger(minute=0),
        id="hourly_scrape",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Scheduler started with jobs: %s", scheduler.get_jobs())

def _run_scrapers():
    try: 
        all_articles = []
        all_articles.extend(scrape_hacker_news())
        all_articles.extend(scrape_techcrunch())
        all_articles.extend(scrape_reddit())

        from app.crud.article import save_articles
        save_articles(all_articles)
        logger.info("Hourly scraper complete: %d articles", len(all_articles))
    except Exception as e:
        logger.exception("Error during hourly scrape")

def _dispatch_digests():
    try: 
        send_email_digest()
        logger.info("Digest dispatch complete")
    except Exception: 
        logger.exception("Error sending digests")

        