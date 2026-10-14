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

def test_procedures(self):
    e = sig("LOGIN_ECHEC", "MOYENNE", "POST /login -> 401")
    self.assertEqual(len(chercher_procedures(e, PROCEDURES)), 1)
    self.assertEqual(chercher_procedures(sig(), PROCEDURES), [])

def test_analyser(self):
    e = sig("LOGIN_ECHEC", "MOYENNE", "POST /login -> 401")
    v = analyser(e, PROCEDURES, 5)
    self.assertEqual(v.niveau, "CRITIQUE")
    self.assertEqual(v.action, "Bloquer l'IP 10.0.0.5")
    self.assertTrue(v.sensible)
    self.assertEqual(e.statut, "ANALYSE")