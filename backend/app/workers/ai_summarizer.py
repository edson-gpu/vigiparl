import asyncio
import hashlib
import logging

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def process_pending_summaries(self):
    try:
        asyncio.run(_process_pending())
    except Exception as exc:
        logger.error(f"AI summarization failed: {exc}")
        raise self.retry(exc=exc)


async def _process_pending():
    from app.database import SessionLocal
    from app.models import AiSummary, Law
    from app.services.claude import claude

    db = SessionLocal()
    try:
        # Lois sans résumé IA
        pending = (
            db.query(Law)
            .outerjoin(AiSummary, Law.id == AiSummary.law_id)
            .filter(AiSummary.id.is_(None))
            .filter(Law.texte_complet.isnot(None))
            .limit(10)
            .all()
        )

        for law in pending:
            try:
                source_hash = hashlib.sha256(law.texte_complet.encode()).hexdigest()
                result = await claude.resume_loi(law.titre, law.texte_complet)
                tags = await claude.generer_tags(law.titre, result["resume"])

                summary = AiSummary(
                    law_id=law.id,
                    resume=result["resume"],
                    impact_citoyen=result["impact_citoyen"],
                    tags=tags,
                    model_version=result["model_version"],
                    prompt_version=result["prompt_version"],
                    token_count=result["token_count"],
                    source_hash=source_hash,
                )
                db.add(summary)
                law.resume_ai = result["resume"]
                law.impact_citoyen = result["impact_citoyen"]
                law.tags = tags
                db.commit()
                logger.info(f"Summarized law {law.an_ref}")
            except Exception as e:
                logger.error(f"Failed to summarize law {law.an_ref}: {e}")
                db.rollback()
    finally:
        db.close()
