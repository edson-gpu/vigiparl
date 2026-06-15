from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "vigiparl",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.scraper", "app.workers.ai_summarizer"],
)

celery_app.conf.beat_schedule = {
    "scrape-scrutins-every-hour": {
        "task": "app.workers.scraper.scrape_scrutins",
        "schedule": crontab(minute=0),
    },
    "process-ai-summaries": {
        "task": "app.workers.ai_summarizer.process_pending_summaries",
        "schedule": crontab(minute=30),
    },
}

celery_app.conf.timezone = "Europe/Paris"
