# Pet Grooming Manager

Gestionale interno per una toelettatura già operativa.

## Stack

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: FastAPI, Python, uv
- Database: PostgreSQL
- Container: Docker Compose

## Avvio locale

### Database

~~~bash
cp .env.example .env
docker compose up -d
~~~

Per fermare il database:

~~~bash
docker compose down
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

Test backend:

~~~bash
cd backend
uv run pytest
~~~

### Frontend

~~~bash
cd frontend
npm install
npm run dev
~~~

Applicazione: `http://localhost:3000`

## Struttura

~~~text
backend/   # API FastAPI
frontend/  # Applicazione Next.js
docker/    # File Docker aggiuntivi, se necessari
docs/      # Documentazione del progetto
~~~

## Stato

Foundation Pack completato: ambiente locale, PostgreSQL, backend FastAPI con health check e frontend Next.js sono pronti.
