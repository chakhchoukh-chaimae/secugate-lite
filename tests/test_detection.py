def test_doublon_different(self):
    vus = set()
    est_deja_vu(sig(), vus)
    autre = sig(); autre.timestamp = "2026-10-05T10:00:01Z"
    self.assertFalse(est_deja_vu(autre, vus))