# Suivi de demandes

Application web interne de suivi de demandes (tickets) : des agents déposent
des demandes, le service support les consulte. Projet personnel réalisé pour
m'exercer à une pile Python / Django moderne.

## Fonctionnalités

- Authentification, avec contrôle d'accès : un agent ne voit que ses demandes,
  le personnel du service voit tout.
- Création, liste (paginée) et détail des demandes.
- API REST (Django REST Framework) avec les mêmes règles d'accès.
- Interface d'administration Django.
- Pages respectant des bases d'accessibilité (HTML sémantique, libellés de
  champs, lien d'évitement, tableaux avec en-têtes).

## Pile technique

Python 3.12 · Django · Django REST Framework · PostgreSQL 16 · Docker / Compose
· Gunicorn + WhiteNoise · GitHub Actions · Ruff · pip-audit

## Lancer le projet avec Docker

```bash
cp .env.example .env     # puis renseigner les valeurs
docker compose up --build
docker compose exec web python manage.py createsuperuser
```

L'application est disponible sur http://localhost:8000.

## Développement local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
docker compose up -d db
python manage.py migrate
python manage.py runserver
```

## Tests et qualité

```bash
python manage.py test        # tests automatisés
ruff check . && ruff format --check .
pip-audit -r requirements.txt
```

La CI GitHub Actions exécute ces contrôles à chaque push, sur un PostgreSQL
réel, et vérifie que l'image Docker se construit.

## API

| Méthode | URL | Description |
|---|---|---|
| GET | `/api/tickets/` | Liste paginée des demandes visibles |
| POST | `/api/tickets/` | Crée une demande |
| GET | `/api/tickets/<id>/` | Détail d'une demande |

Authentification par session ou HTTP Basic (développement). Le demandeur et le
statut sont fixés côté serveur.

```bash
curl -u agent1 http://localhost:8000/api/tickets/
```

## Choix techniques

- Règle d'accès centralisée dans le modèle (`visibles_par`), utilisée par les
  vues web et l'API, avec des tests dédiés.
- Secrets et configuration lus depuis l'environnement (`.env` non versionné).
- Conteneur exécuté sans droits root.

## Pistes d'amélioration

Modification du statut et affectation par le personnel,
authentification unique (OIDC), déploiement continu.