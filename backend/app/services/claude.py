import anthropic

from app.config import settings

PROMPT_VERSION = "v1.0"

SYSTEM_RESUME = """Tu es un assistant de transparence parlementaire pour VigiParl.
Tu résumes des textes de loi français de façon neutre, factuelle et accessible à un niveau lycée.
Tu ne prends jamais de position politique. Tu cites toujours les faits, jamais des opinions.
Réponds uniquement en français."""

SYSTEM_TAGS = """Tu es un assistant de classification thématique de textes législatifs.
Extrait uniquement les thèmes pertinents parmi : economie, immigration, sante, environnement,
education, justice, defense, logement, travail, retraites, fiscalite, numerique, agriculture, energie, social.
Réponds en JSON uniquement : {"tags": ["theme1", "theme2"]}"""


class ClaudeService:
    def __init__(self):
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def resume_loi(self, titre: str, texte: str) -> dict:
        prompt = f"""Loi : {titre}

Texte complet :
{texte[:15000]}

Fournis :
1. RESUME (5 lignes max, niveau lycée, ce que fait concrètement cette loi)
2. IMPACT_CITOYEN (2 lignes : "Concrètement, cette loi signifie que...")

Format de réponse :
RESUME: ...
IMPACT_CITOYEN: ..."""

        message = await self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            temperature=0.1,
            system=SYSTEM_RESUME,
            messages=[{"role": "user", "content": prompt}],
        )

        content = message.content[0].text
        lines = content.strip().split("\n")
        resume = ""
        impact = ""
        current = None
        for line in lines:
            if line.startswith("RESUME:"):
                current = "resume"
                resume = line.replace("RESUME:", "").strip()
            elif line.startswith("IMPACT_CITOYEN:"):
                current = "impact"
                impact = line.replace("IMPACT_CITOYEN:", "").strip()
            elif current == "resume":
                resume += " " + line.strip()
            elif current == "impact":
                impact += " " + line.strip()

        return {
            "resume": resume.strip(),
            "impact_citoyen": impact.strip(),
            "model_version": "claude-sonnet-4-6",
            "prompt_version": PROMPT_VERSION,
            "token_count": message.usage.input_tokens + message.usage.output_tokens,
        }

    async def generer_tags(self, titre: str, resume: str) -> list[str]:
        message = await self._client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            temperature=0.0,
            system=SYSTEM_TAGS,
            messages=[{"role": "user", "content": f"Titre: {titre}\nRésumé: {resume}"}],
        )
        import json
        try:
            data = json.loads(message.content[0].text)
            return data.get("tags", [])
        except Exception:
            return []

    async def score_coherence(self, declaration: str, vote: str, contexte: str) -> dict:
        message = await self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            temperature=0.1,
            system=SYSTEM_RESUME,
            messages=[{
                "role": "user",
                "content": f"""Déclaration publique : {declaration}
Vote réel : {vote}
Contexte : {contexte}

Évalue la cohérence entre 0 et 100 et explique en 2 phrases.
Format : SCORE: X\nEXPLICATION: ...""",
            }],
        )
        content = message.content[0].text
        score = 50
        explication = ""
        for line in content.split("\n"):
            if line.startswith("SCORE:"):
                try:
                    score = int(line.replace("SCORE:", "").strip())
                except ValueError:
                    pass
            elif line.startswith("EXPLICATION:"):
                explication = line.replace("EXPLICATION:", "").strip()
        return {"score": score, "explication": explication}


claude = ClaudeService()
