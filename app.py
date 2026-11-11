# ============================================================
# Application de consultation des notes des étudiants
# ============================================================

import os
import sqlite3
import auth
import math

from flask import Flask, jsonify, request

app = Flask(__name__)

# Fichier où sont conservées les notes de l'école
DB = "notes.db"


# Prépare le registre des notes au démarrage de l'application
def init_db():
    with sqlite3.connect(DB) as con:
        # Chaque note concerne un étudiant, dans un module
        con.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, etudiant TEXT, module TEXT, note REAL)"
        )
        # Si le registre est vide, on y inscrit deux notes d'exemple
        if con.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
                [("Amina", "DevSecOps", 15.5), ("Youssef", "DevSecOps", 12.0)],
            )


init_db()


# Page d'accueil : l'étudiant y trouve le lien vers les notes
@app.route("/")
def accueil():
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        "<title>Notes des etudiants</title></head><body>"
        "<h1>Consultation des notes</h1>"
        "<p><a href='/notes'>Voir les notes</a></p></body></html>"
    )


# Indique que le service des notes est disponible
@app.route("/health")
def health():
    return {"status": "ok", "version": "1.0"}


# Consultation des notes : toutes les notes,
# ou seulement celles d'un étudiant si on donne son nom
# Exemple : /notes?etudiant=Amina
@app.route("/notes")
def lister_notes():
    # Nom de l'étudiant recherché (facultatif)
    etudiant = request.args.get("etudiant", "")
    with sqlite3.connect(DB) as con:
        rows = con.execute(
            "SELECT id, etudiant, module, note FROM notes WHERE etudiant LIKE ?",
            (f"%{etudiant}%",),
        ).fetchall()
    # Pour chaque note : l'étudiant, le module et la note obtenue
    return jsonify(
        [{"id": r[0], "etudiant": r[1], "module": r[2], "note": r[3]} for r in rows]
    )

# Modification d'une note par l'enseignant
@app.route("/notes/<note_id>", methods=["PUT"])
def modifier_note(note_id):
    try:
        # 1. Vérifier l'identité
        utilisateur = auth.utilisateur_connecte()

        if utilisateur is None:
            return "Authentification requise", 401

        # 2. Vérifier le rôle
        if utilisateur.get("role") != "enseignant":
            return "Accès interdit", 403

        # 3. Vérifier la note envoyée
        donnees = request.get_json(silent=True)

        if not isinstance(donnees, dict):
            return "Données invalides", 400

        nouvelle_note = donnees.get("note")

        if (isinstance(nouvelle_note, bool)
                or not isinstance(nouvelle_note, (int, float))
                or not math.isfinite(nouvelle_note)
                or not 0 <= nouvelle_note <= 20):
            return "Note invalide", 400

        # 4. Vérifier le module de la note
        with sqlite3.connect(DB) as con:
            resultat = con.execute(
                "SELECT module FROM notes WHERE id = ?",
                (note_id,)
            ).fetchone()

            if resultat is None:
                return "Note introuvable", 404

            if resultat[0] != utilisateur.get("module"):
                return "Accès interdit", 403

            # 5. Modifier la note avec une requête sécurisée
            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?",
                (nouvelle_note, note_id)
            )

        return "OK", 200

    except Exception:
        # Ne jamais exposer les détails techniques
        return "Erreur interne", 500