# ============================================================
# Vérifications automatiques : l'application rend-elle le service attendu ?
# ============================================================

from app import app

client = app.test_client()


# Un visiteur peut ouvrir la page d'accueil
def test_accueil():
    reponse = client.get("/")
    assert reponse.status_code == 200


# Le service des notes signale qu'il est disponible
def test_health():
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.get_json()["status"] == "ok"


# La liste contient au moins les deux notes d'exemple
def test_liste_notes():
    reponse = client.get("/notes")
    assert reponse.status_code == 200
    assert len(reponse.get_json()) >= 2


# Un étudiant qui cherche son nom retrouve sa note (Amina : 15,5)
def test_recherche_etudiant():
    reponse = client.get("/notes?etudiant=Amina")
    assert reponse.get_json()[0]["note"] == 15.5
    
def test_version():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["version"] == "1.0"
    