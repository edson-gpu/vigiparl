import asyncio
import logging

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def scrape_scrutins(self):
    try:
        asyncio.run(_scrape_scrutins())
    except Exception as exc:
        logger.error(f"Scraping failed: {exc}")
        raise self.retry(exc=exc)


async def _scrape_scrutins():
    from app.database import SessionLocal
    from app.models import Law
    from app.services.assemblee import assemblee

    logger.info("Scraping scrutins from Assemblée Nationale...")
    data = await assemblee.get_scrutins()
    db = SessionLocal()
    try:
        scrutins = data.get("scrutins", {}).get("scrutin", [])
        new_count = 0
        for scrutin in scrutins:
            an_ref = scrutin.get("uid", "")
            existing = db.query(Law).filter(Law.an_ref == an_ref).first()
            if not existing:
                law = Law(
                    an_ref=an_ref,
                    titre=scrutin.get("titre", ""),
                    statut="votee" if scrutin.get("syntheseVote", {}).get("typeVote") else "en_attente",
                    pour_count=int(scrutin.get("syntheseVote", {}).get("nombreVotants", 0) or 0),
                )
                db.add(law)
                new_count += 1
        db.commit()
        logger.info(f"Scraped {new_count} new scrutins")
    finally:
        db.close()
        await assemblee.close()
