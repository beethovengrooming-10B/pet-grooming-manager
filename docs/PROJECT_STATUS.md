# Project Status

## Progetto

**Pet Grooming Manager**

Gestionale reale per una toelettatura operativa.

## Stato generale

**Sprint 1 completato**

Il backend dispone ora delle funzionalità base per la gestione dei clienti e degli animali.

## Sprint completati

### Sprint 0 - Foundation

**COMPLETATO**

- Repository GitHub.
- Struttura monorepo.
- Directory `backend`.
- Directory `frontend`.
- Directory `docs`.
- Directory `docker`.
- Ambiente WSL2 e VS Code Remote WSL.
- Configurazione iniziale del progetto.

Dettagli:

```text
docs/sprints/SPRINT_00_FOUNDATION.md
```

### Sprint 1 - Animal Management

**COMPLETATO**

- Modello `Animal`.
- Relazione cliente-animale.
- Creazione animali.
- Lista animali per cliente.
- Recupero singolo animale.
- Modifica animali.
- Eliminazione animali.
- Validazione Pydantic.
- Cascade delete.
- Migrazione Alembic.
- Test automatici.
- Verifica manuale con curl.

Dettagli:

```text
docs/sprints/SPRINT_01_ANIMALS.md
```

## API attualmente disponibili

### Health check

```text
GET /health
```

### Clienti

```text
POST   /clients
GET    /clients
GET    /clients/{client_id}
PUT    /clients/{client_id}
DELETE /clients/{client_id}
```

### Animali

```text
POST   /clients/{client_id}/animals
GET    /clients/{client_id}/animals
GET    /animals/{animal_id}
PUT    /animals/{animal_id}
DELETE /animals/{animal_id}
```

## Test

Comando ufficiale:

```bash
cd backend
uv run pytest
```

Ultimo risultato verificato:

```text
17 passed, 1 warning
```

Il warning presente è non bloccante e riguarda una deprecation warning dell'integrazione Starlette/httpx usata da `TestClient`.

## Verifica manuale

Le API Animali sono state verificate manualmente con `curl`.

Verifiche completate:

- Creazione animale.
- Recupero animale.
- Modifica animale.
- Lista animali.
- Eliminazione animale.
- Risposta `404` per risorsa inesistente.
- Risposta `422` per dati non validi.

## Configurazione tecnica

### Frontend

- Next.js.
- React.
- TypeScript.
- Tailwind CSS.
- shadcn/ui.
- TanStack Query.
- React Hook Form.
- Zod.

### Backend

- FastAPI.
- SQLAlchemy 2.
- Alembic.
- Pydantic.
- uv.

### Database

- PostgreSQL.

### Testing

- pytest.
- Playwright.
- Bruno.
- curl per verifiche manuali.

### Hosting previsto

- Vercel.
- Railway oppure Render.

## Regole di progetto

- MVP first.
- Una feature alla volta.
- Nessun overengineering.
- API RESTful.
- Database progettato con cura.
- Migrazioni tramite Alembic.
- Test dove portano valore.
- Documentazione aggiornata a ogni sprint.
- Nessuna funzionalità fuori scope senza decisione esplicita.

## Backlog futuro

Non implementare ora:

- Dashboard.
- Statistiche.
- Clienti abituali.
- Clienti persi.
- Lista d'attesa.
- WhatsApp.
- Pagamenti.
- AI.
- Report.

## Prossimo sprint proposto

### Sprint 2 - Frontend Foundation

Possibili attività:

- Configurazione iniziale Next.js.
- Layout principale.
- Configurazione Tailwind e shadcn/ui.
- Client API.
- Prima pagina clienti.
- Collegamento frontend-backend.

Lo scope definitivo deve essere approvato prima dell'implementazione.