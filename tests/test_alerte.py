
import unittest
from src.alerte import choisir_canal


class TestAlerte(unittest.TestCase):

    def test_canaux(self):
        self.assertEqual(choisir_canal("CRITIQUE"), "TELEPHONE")
        self.assertEqual(choisir_canal("ELEVEE"), "SLACK")
        self.assertEqual(choisir_canal("MOYENNE"), "EMAIL")
        self.assertEqual(choisir_canal("FAIBLE"), "TABLEAU")

    def test_canal_invalide(self):
        with self.assertRaises(ValueError):
            choisir_canal("URGENT")


if __name__ == "__main__":
    unittest.main()
