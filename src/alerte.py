
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
