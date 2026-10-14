
from src.contrat import Signal, Verdict, Alerte


def choisir_canal(niveau: str) -> str:
    """Choisit le canal de notification selon le niveau de gravité."""
    canaux = {
        "CRITIQUE": "TELEPHONE",
        "ELEVEE": "SLACK",
        "MOYENNE": "EMAIL",
        "FAIBLE": "TABLEAU",
    }

    if niveau not in canaux:
        raise ValueError(f"Niveau inconnu : {niveau}")

    return canaux[niveau]


def rediger(sig: Signal, verdict: Verdict) -> str:
    """Génère le texte de l'alerte à partir du signal et du verdict."""
    return "\n".join([
        f"[{verdict.niveau}] Cible : {sig.cible}",
        f"Signal : {sig.message}",
        f"Explication : {verdict.explication}",
        f"Action proposee : {verdict.action}",
        f"Sources : {', '.join(verdict.sources)}",
    ])


def alerter(sig: Signal, verdict: Verdict, journal: list) -> Alerte:
    """Crée une alerte, l'enregistre et met à jour le statut du signal."""
    alerte = Alerte(
        signal_id=sig.id,
        canal=choisir_canal(verdict.niveau),
        destinataire="equipe-secu",
        texte=rediger(sig, verdict),
    )

    journal.append(alerte)
    sig.statut = "ALERTE"

    return alerte


def valider_action(verdict: Verdict, reponse: str) -> bool:
    """Vérifie la confirmation humaine pour une action sensible."""
    if not verdict.sensible:
        return True

    reponse = "".join(reponse.split()).lower()
    return reponse in ("o", "oui", "ok", "yes")

