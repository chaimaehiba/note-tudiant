# Exigences de sécurité de l'application des notes

| # | Exigence : « Le système doit… » | Vérification | Étape du SDLC | Test |
|---|---|---|---|---|
| 1 | utiliser des requêtes SQL sécurisées pour éviter les injections SQL. | Recherche avec une entrée malveillante. | Développement | S1 |
| 2 | authentifier l'utilisateur avant toute modification. | Vérifier la présence d'un jeton valide. | Développement | S2 |
| 3 | autoriser uniquement les enseignants à modifier les notes. | Vérifier le rôle de l'utilisateur. | Conception | S3 |
| 4 | vérifier que l'enseignant appartient au module concerné. | Vérifier le module de l'enseignant. | Conception | S4 |
| 5 | valider les notes entre 0 et 20. | Envoyer des valeurs invalides. | Développement | S5 |
| 6 | protéger les informations internes en cas d'erreur serveur. | Vérifier le message retourné. | Tests | S7 |