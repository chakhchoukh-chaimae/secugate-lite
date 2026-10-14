
import unittest

from src.alerte import (
    choisir_canal,
    rediger,
    alerter,
    valider_action,
)
from src.contrat import Signal, Verdict


def exemple(sensible=True, niveau="CRITIQUE"):
    sig = Signal(
        "SIG-00125",
        "2026-10-05T10:01:31Z",
        "ACCES",
        "192.168.1.15",
        "web-app",
        "LOGIN_ECHEC",
        "MOYENNE",
        "POST /login -> 401 depuis 192.168.1.x",
    )

    verdict = Verdict(
        "SIG-00125",
        niveau,
        "Echecs de connexion",
        "Bloquer l'IP 192.168.1.15",
        sensible,
        ["ACCES"],
    )

    return sig, verdict


class TestAlerte(unittest.TestCase):

    # Tests de choisir_canal

    def test_canaux(self):
        self.assertEqual(choisir_canal("CRITIQUE"), "TELEPHONE")
        self.assertEqual(choisir_canal("ELEVEE"), "SLACK")
        self.assertEqual(choisir_canal("MOYENNE"), "EMAIL")
        self.assertEqual(choisir_canal("FAIBLE"), "TABLEAU")

    def test_canal_invalide(self):
        with self.assertRaises(ValueError):
            choisir_canal("URGENT")

    # Tests de rediger

    def test_rediger(self):
        sig, verdict = exemple()
        lignes = rediger(sig, verdict).split("\n")

        self.assertEqual(len(lignes), 5)
        self.assertEqual(lignes[0], "[CRITIQUE] Cible : web-app")
        self.assertEqual(
            lignes[1],
            "Signal : POST /login -> 401 depuis 192.168.1.x",
        )
        self.assertEqual(lignes[2], "Explication : Echecs de connexion")
        self.assertEqual(
            lignes[3],
            "Action proposee : Bloquer l'IP 192.168.1.15",
        )
        self.assertEqual(lignes[4], "Sources : ACCES")

    def test_rediger_plusieurs_sources(self):
        sig, verdict = exemple()
        verdict.sources = ["ACCES", "SCAN"]

        self.assertEqual(
            rediger(sig, verdict).split("\n")[4],
            "Sources : ACCES, SCAN",
        )

    # Tests de alerter

    def test_alerter(self):
        sig, verdict = exemple()
        journal = []

        a = alerter(sig, verdict, journal)

        self.assertEqual(a.signal_id, "SIG-00125")
        self.assertEqual(a.canal, "TELEPHONE")
        self.assertEqual(a.destinataire, "equipe-secu")
        self.assertEqual(a.texte, rediger(sig, verdict))
        self.assertEqual(journal, [a])
        self.assertEqual(sig.statut, "ALERTE")

    def test_alerter_historise(self):
        sig, verdict = exemple()
        journal = []

        alerter(sig, verdict, journal)
        alerter(sig, verdict, journal)

        self.assertEqual(len(journal), 2)

    def test_alerter_niveau_invalide(self):
        sig, verdict = exemple(niveau="URGENT")
        journal = []

        with self.assertRaises(ValueError):
            alerter(sig, verdict, journal)

        self.assertEqual(journal, [])

    # Tests de valider_action

    def test_validation(self):
        _, verdict = exemple()

        self.assertTrue(valider_action(verdict, " OUI "))
        self.assertFalse(valider_action(verdict, "n"))

    def test_validation_reponses_acceptees(self):
        _, verdict = exemple()

        for reponse in ("o", "O", "oui", "Ok", "YES", "  yes  "):
            with self.subTest(reponse=reponse):
                self.assertTrue(valider_action(verdict, reponse))

    def test_validation_reponses_refusees(self):
        _, verdict = exemple()

        for reponse in ("", "non", "no", "peut-etre"):
            with self.subTest(reponse=reponse):
                self.assertFalse(valider_action(verdict, reponse))

    def test_validation_action_non_sensible(self):
        _, verdict = exemple(sensible=False)

        self.assertTrue(valider_action(verdict, "n"))


if __name__ == "__main__":
    unittest.main()
