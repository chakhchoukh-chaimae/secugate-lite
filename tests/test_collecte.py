import unittest

from src.collecte import masquer_ip

LIGNE = "2026-10-05 10:01:10 192.168.1.15 POST /login 401"


class TestCollecte(unittest.TestCase):
    def test_masquer_ip(self):
        self.assertEqual(masquer_ip("192.168.1.15"), "192.168.1.x")

    def test_masquer_ip_invalide(self):
        with self.assertRaises(ValueError):
            masquer_ip("1.2.3")


if __name__ == "__main__":
    unittest.main()