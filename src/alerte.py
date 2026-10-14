from src.contrat import Alerte

def choisir_canal(niveau: str) -> str:
    canaux = {
        "CRITIQUE": "TELEPHONE",
        "ELEVEE": "SLACK",
        "MOYENNE": "EMAIL",
        "FAIBLE": "TABLEAU",
    }

    if niveau not in canaux:
        raise ValueError(f"Niveau inconnu : {niveau}")

    return canaux[niveau]

def rediger(sig, verdict) -> str:
    return "\n".join([
        f"[{verdict.niveau}] Cible : {sig.cible}",
        f"Signal : {sig.message}",
        f"Explication : {verdict.explication}",
        f"Action proposee : {verdict.action}",
        f"Sources : {', '.join(verdict.sources)}",
    ])

def alerter(sig, verdict, journal):
    alerte = Alerte(
        signal_id=sig.id,
        canal=choisir_canal(verdict.niveau),
        destinataire="equipe-secu",
        texte=rediger(sig, verdict),
    )
    journal.append(alerte)
    sig.statut = "ALERTE"
    return alerte
