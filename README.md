# SecuGate-Lite
Groupe : PINKERSTEAMS
Mini-plateforme de surveillance des accès d'une application : trois agents
(Collecte, Détection, Alerte) qui échangent via un contrat commun
(src/contrat.py).
## Équipe
 - Chaimae Chakhchoukh agent collection (A)
 - Hayoun Ferdaous: agent detection (B)
 - Bekkali Salsabil : agent alerte (C)
secugate-lite/
├── README.md
├── .gitignore
├── main.py (démonstration de bout en bout)
├── src/
│ ├── __init__.py (fichier vide)
│ ├── contrat.py (contrat d’échange commun, fourni)
│ ├── collecte.py (A : Agent 1)
│ ├── detection.py (B : Agent 2)
│ ├── alerte.py (C : Agent 3)
│ └── workflow.py (enchaîne les trois agents, fourni)
└── tests/
├── __init__.py (fichier vide)
├── test_collecte.py (A)
├── test_detection.py (B)
>>>>>>> c549d0ec126d25260b7ffdb8c710d3ce92164f50
└── test_alerte.py (C)