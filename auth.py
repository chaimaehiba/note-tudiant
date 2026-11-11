import json
import os
from flask import request

FICHIER_JETONS = os.environ.get("FICHIER_JETONS", "jetons.json")


def utilisateur_connecte():
    entete = request.headers.get("Authorization", "")

    if not entete.startswith("Bearer "):
        return None

    try:
        with open(FICHIER_JETONS, encoding="utf-8") as fichier:
            jetons = json.load(fichier)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    return jetons.get(entete.removeprefix("Bearer "))