
import unittest
from src.alerte import choisir_canal, rediger, alerter
from src.contrat import Signal, Verdict


def exemple(sensible=True, niveau="CRITIQUE"):
    s = Signal(
        "SIG-00125", "2026-10-05T10:01:31Z", "ACCES",
        "192.168.1.15", "web-app", "LOGIN_ECHEC", "MOYENNE",
        "POST /login -> 401 depuis 192.168.1.x"
    )
    v = Verdict(
        "SIG-00125", niveau, "Echecs de connexion",
        "Bloquer l'IP 192.168.1.15", sensible, ["ACCES"]
    )
    return s, v


class TestAlerte(unittest.TestCase):

    def test_canaux(self):
        self.assertEqual(choisir_canal("CRITIQUE"), "TELEPHONE")
        self.assertEqual(choisir_canal("ELEVEE"), "SLACK")
        self.assertEqual(choisir_canal("MOYENNE"), "EMAIL")
        self.assertEqual(choisir_canal("FAIBLE"), "TABLEAU")

    def test_canal_invalide(self):
        with self.assertRaises(ValueError):
            choisir_canal("URGENT")

    def test_rediger(self):
        s, v = exemple()
        lignes = rediger(s, v).split("\n")
        self.assertEqual(len(lignes), 5)
        self.assertEqual(lignes[0], "[CRITIQUE] Cible : web-app")
        self.assertEqual(lignes[1], "Signal : POST /login -> 401 depuis 192.168.1.x")
        self.assertEqual(lignes[2], "Explication : Echecs de connexion")
        self.assertEqual(lignes[3], "Action proposee : Bloquer l'IP 192.168.1.15")
        self.assertEqual(lignes[4], "Sources : ACCES")

    def test_rediger_plusieurs_sources(self):
        s, v = exemple()
        v.sources = ["ACCES", "SCAN"]
        self.assertEqual(
            rediger(s, v).split("\n")[4],
            "Sources : ACCES, SCAN"
        )

    
    def test_alerter(self):
        s, v = exemple()
        journal = []
        a = alerter(s, v, journal)

        self.assertEqual(a.signal_id, "SIG-00125")
        self.assertEqual(a.canal, "TELEPHONE")
        self.assertEqual(a.destinataire, "equipe-secu")
        self.assertEqual(a.texte, rediger(s, v))
        self.assertEqual(journal, [a])
        self.assertEqual(s.statut, "ALERTE")

    def test_alerter_historise(self):
        s, v = exemple()
        journal = []
        alerter(s, v, journal)
        alerter(s, v, journal)
        self.assertEqual(len(journal), 2)

    def test_alerter_niveau_invalide(self):
        s, v = exemple(niveau="URGENT")
        journal = []
        with self.assertRaises(ValueError):
            alerter(s, v, journal)
        self.assertEqual(journal, [])



if __name__ == "__main__":
    unittest.main()
