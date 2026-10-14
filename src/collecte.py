import re

from src.contrat import Signal


def masquer_ip(ip: str) -> str:
    parties = ip.split(".")
    if len(parties) != 4:
        raise ValueError(f"Adresse IP invalide : {ip}")
    return ".".join(parties[:3] + ["x"])


def masquer_parametres(chemin: str) -> str:
    return re.sub(r"(?i)\b(token|password|session|key)=[^&\s]*",
                  lambda m: m.group(1) + "=[MASQUE]", chemin)


def normaliser_acces(ligne: str, numero: int, cible: str = "web-app") -> Signal:
    champs = ligne.split()
    if len(champs) < 6:
        raise ValueError(f"Ligne invalide : {ligne}")
    date, heure, ip, methode, chemin, statut = champs[:6]
    statut = int(statut)
    chemin_nu = chemin.split("?")[0]

    if chemin_nu == "/login" and statut in (401, 403):
        type_ = "LOGIN_ECHEC"
    else:
        type_ = "ACCES"

    if statut >= 500:
        gravite = "ELEVEE"
    elif statut >= 400:
        gravite = "MOYENNE"
    else:
        gravite = "FAIBLE"

    message = (f"{methode} {masquer_parametres(chemin)} -> {statut} "
               f"depuis {masquer_ip(ip)}")
    return Signal(f"SIG-{numero:05d}", f"{date}T{heure}Z", "ACCES", ip,
                  cible, type_, gravite, message)


def normaliser_scan(rapport: dict, numero: int) -> Signal:
    raise NotImplementedError
