# Sprint 0 — Foundation Pack

## Stato

**Completato**

## Obiettivo

Preparare un ambiente locale stabile e riproducibile per lo sviluppo del Pet Grooming Manager.

## Attività completate

### Struttura repository

Creata e mantenuta la struttura iniziale del monorepo:

~~~text
pet-grooming-manager/
├── backend/
├── frontend/
├── docker/
├── docs/
├── .editorconfig
├── .gitignore
├── .env.example
├── README.md
└── docker-compose.yml
~~~

### Ambiente di sviluppo

- WSL e VS Code Remote WSL configurati.
- Docker Desktop collegato a WSL.
- Node.js LTS e npm installati.
- `uv` installato per la gestione del backend Python.
- Git configurato per il repository.

### Database

- PostgreSQL 17 avviato tramite Docker Compose.
- Volume Docker persistente configurato.
- Database locale `pet_grooming` verificato tramite query SQL.

### Backend

- Progetto Python inizializzato con `uv`.
- FastAPI e Uvicorn installati.
- Endpoint `GET /health` creato.
- Endpoint verificato tramite browser e documentazione Swagger.
- Test pytest per health check creato e superato.

### Frontend

- Applicazione Next.js inizializzata.
- TypeScript, Tailwind CSS, ESLint e App Router configurati.
- Avvio locale verificato.
- Lint superato.
- Build di produzione superata.

### Gestione clienti

- Modello `Client` creato.
- Migrazione Alembic per la tabella `clients`.
- API per creazione, ricerca, modifica ed eliminazione.
- Validazione degli input tramite Pydantic.
- Test API per il ciclo CRUD.
- Form frontend per creazione e modifica.
- Ricerca clienti.
- Eliminazione con conferma.
- Flusso frontend → API → PostgreSQL verificato manualmente.

### Documentazione

- README aggiornato con istruzioni di avvio.
- Stato del progetto documentato in `docs/PROJECT_STATUS.md`.
- Resoconto Sprint 0 creato in questo file.

## Verifiche eseguite

| Verifica | Risultato |
| --- | --- |
| `docker compose config` | Superata |
| Connessione a PostgreSQL | Superata |
| `uv run pytest` | 8 test superati |
| `npm run lint` | Superato |
| `npm run build` | Superata |
| Backend su browser | Verificato |
| Frontend su browser | Verificato |
| Creazione cliente | Verificata |
| Ricerca cliente | Verificata |
| Modifica cliente | Verificata |
| Eliminazione cliente | Verificata |

## Commit

Commit finale dello Sprint 0:

~~~text
6788c35 feat(sprint-0): complete foundation and clients management
~~~

Commit precedente incluso nella cronologia:

~~~text
3eb15c5 chore: complete sprint 0 foundation
~~~

## Note

Il test backend mostra un avviso di deprecazione proveniente da una dipendenza FastAPI/Starlette. Non blocca il funzionamento e non richiede una modifica immediata.

## Prossimo sprint

Sprint 1 — Gestione Animali.
