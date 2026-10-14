def test_doublon_different(self):
    vus = set()
    est_deja_vu(sig(), vus)
    autre = sig(); autre.timestamp = "2026-10-05T10:00:01Z"
    self.assertFalse(est_deja_vu(autre, vus))

def test_compter(self):
    c = {}
    e = sig("LOGIN_ECHEC", "MOYENNE")
    self.assertEqual(compter_echecs(e, c), 1)
    self.assertEqual(compter_echecs(e, c), 2)
    self.assertEqual(compter_echecs(sig(), c), 0)