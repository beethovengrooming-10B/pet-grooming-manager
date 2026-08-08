# Stato del progetto

## Progetto

**Pet Grooming Manager** è un gestionale interno per una toelettatura già operativa.

## Stato attuale

**Sprint 0 — Foundation Pack: completato**

Il progetto ha una base locale funzionante e verificata:

- repository Git configurato;
- PostgreSQL in Docker Compose;
- backend FastAPI con endpoint health check;
- test backend attivi;
- frontend Next.js configurato;
- lint e build frontend verificati.

## Come avviare il progetto

### Database

~~~bash
cp .env.example .env
docker compose up -d
~~~

### Backend

~~~bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
~~~

- API: `http://127.0.0.1:8000`
- Documentazione API: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

### Frontend

~~~bash
cd frontend
npm install
npm run dev
~~~

- Applicazione: `http://localhost:3000`

## Prossimo sprint

**Sprint 1 — Gestione Clienti**

Obiettivo: definire e implementare la prima parte del gestionale clienti:

- campi e regole del cliente;
- modello database;
- migrazione Alembic;
- API CRUD e ricerca;
- test API;
- prima interfaccia frontend.

## Problemi noti

Nessun blocco attivo.

Il test FastAPI mostra un avviso di deprecazione proveniente da una dipendenza esterna. Il test passa correttamente; l’avviso verrà rivalutato quando aggiorneremo le dipendenze del backend.