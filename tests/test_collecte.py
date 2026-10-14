import unittest

from src.collecte import masquer_ip, masquer_parametres

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


if __name__ == "__main__":
    unittest.main()