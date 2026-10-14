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
    raise NotImplementedError


def normaliser_scan(rapport: dict, numero: int) -> Signal:
    raise NotImplementedError
