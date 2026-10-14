import unittest

from src.collecte import masquer_ip, masquer_parametres, normaliser_acces

LIGNE = "2026-10-05 10:01:10 192.168.1.15 POST /login 401"


class TestCollecte(unittest.TestCase):
    def test_masquer_ip(self):
        self.assertEqual(masquer_ip("192.168.1.15"), "192.168.1.x")

    def test_masquer_ip_invalide(self):
        with self.assertRaises(ValueError):
            masquer_ip("1.2.3")

    def test_masquer_parametres(self):
        self.assertEqual(masquer_parametres("/api?id=3&token=abc123"),
                         "/api?id=3&token=[MASQUE]")

    def test_masquer_parametres_casse(self):
        self.assertEqual(masquer_parametres("/x?PASSWORD=abc&id=1"),
                         "/x?PASSWORD=[MASQUE]&id=1")

    def test_normaliser_acces(self):
        sig = normaliser_acces(LIGNE, 42)
        self.assertEqual(sig.id, "SIG-00042")
        self.assertEqual(sig.timestamp, "2026-10-05T10:01:10Z")
        self.assertEqual(sig.source, "ACCES")
        self.assertEqual(sig.ip, "192.168.1.15")
        self.assertEqual(sig.type, "LOGIN_ECHEC")
        self.assertEqual(sig.message, "POST /login -> 401 depuis 192.168.1.x")

    def test_acces_normal(self):
        sig = normaliser_acces("2026-10-05 10:00:01 10.0.0.5 GET /home 200", 1)
        self.assertEqual(sig.type, "ACCES")
        self.assertEqual(sig.gravite, "FAIBLE")

    def test_gravite_4xx_et_5xx(self):
        self.assertEqual(
            normaliser_acces("2026-10-05 10:00:01 10.0.0.5 GET /x 404", 1).gravite,
            "MOYENNE")
        self.assertEqual(
            normaliser_acces("2026-10-05 10:00:01 10.0.0.5 GET /x 500", 1).gravite,
            "ELEVEE")

    def test_ligne_trop_courte(self):
        with self.assertRaises(ValueError):
            normaliser_acces("2026-10-05 10:00:01 10.0.0.5", 1)


if __name__ == "__main__":
    unittest.main()