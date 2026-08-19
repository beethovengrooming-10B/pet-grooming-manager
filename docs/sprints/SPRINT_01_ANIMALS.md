# Sprint 1 - Animal Management

## Stato

**COMPLETATO**

## Obiettivo

Implementare la gestione degli animali collegati ai clienti esistenti.

## Funzionalità implementate

- Creazione di un animale.
- Lista degli animali appartenenti a un cliente.
- Recupero di un singolo animale.
- Modifica di un animale.
- Eliminazione di un animale.
- Validazione dei dati.
- Relazione uno-a-molti tra clienti e animali.
- Cascade delete degli animali alla cancellazione del cliente.
- Migrazione Alembic.
- Test automatici delle API.

## Decisioni architetturali

- È stato mantenuto lo stack esistente: FastAPI, SQLAlchemy, Pydantic e Alembic.
- È stato introdotto un modello dedicato `Animal`.
- Ogni animale appartiene a un solo cliente tramite `client_id`.
- Un cliente può avere più animali.
- Sono stati utilizzati endpoint REST con naming prevedibile.
- La validazione viene eseguita al confine dell'API tramite gli schemi Pydantic.
- La relazione database utilizza il cascade delete.
- Non sono state introdotte nuove librerie o complessità non necessarie.

## Modello dati

L'entità `Animal` contiene:

- `id`.
- `client_id`.
- `name`.
- `species`.
- `breed`.
- `size`.
- `coat_type`.
- `age`.
- `notes`.
- `created_at`.
- `updated_at`.

Il campo `age` accetta valori maggiori o uguali a zero. I valori negativi vengono rifiutati con HTTP 422.

## API disponibili

| Metodo | Endpoint | Descrizione |
|---|---|---|
| POST | `/clients/{client_id}/animals` | Crea un animale per un cliente |
| GET | `/clients/{client_id}/animals` | Restituisce gli animali di un cliente |
| GET | `/animals/{animal_id}` | Restituisce un animale |
| PUT | `/animals/{animal_id}` | Modifica un animale |
| DELETE | `/animals/{animal_id}` | Elimina un animale |

## Validazione verificata

Sono stati verificati i seguenti casi:

- Payload valido accettato.
- Nome vuoto rifiutato.
- Età negativa rifiutata.
- Specie non valida rifiutata.
- Cliente inesistente rifiutato con HTTP 404.
- Animale inesistente rifiutato con HTTP 404.

## Database

È stata creata la migrazione Alembic:

```text
backend/alembic/versions/a53b4133082e_create_animals_table.py
```

La migrazione crea la tabella degli animali e la chiave esterna verso i clienti.

## Test automatici

I test sono stati eseguiti dalla directory `backend`:

```bash
cd /home/leonardo/projects/pet-grooming-manager/backend
uv run pytest
```

Risultato:

```text
17 passed, 1 warning
```

Test eseguiti:

- 9 test per gli animali.
- 7 test per i clienti.
- 1 test per l'health check.

L'unico warning è una deprecation warning non bloccante relativa all'integrazione Starlette/httpx utilizzata da `TestClient`.

## Test manuali con curl

Sono stati verificati:

- Cancellazione di un animale esistente con risposta `204 No Content`.
- Cancellazione di un animale inesistente con risposta `404 Not Found`.
- Validazione di un'età negativa con risposta `422 Unprocessable Entity`.

Esempio:

```bash
curl -i -X DELETE http://127.0.0.1:8000/animals/1
```

## Configurazione test

È stata aggiunta la configurazione pytest in:

```text
backend/pyproject.toml
```

Configurazione:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

Questo consente di eseguire i test dalla directory `backend` mantenendo gli import:

```python
from app.main import app
```

## File aggiunti o modificati

- `backend/app/api/animals.py`
- `backend/app/models/animal.py`
- `backend/app/schemas/animal.py`
- `backend/app/models/client.py`
- `backend/app/models/__init__.py`
- `backend/app/main.py`
- `backend/alembic/versions/a53b4133082e_create_animals_table.py`
- `backend/tests/test_animals.py`
- `backend/pyproject.toml`

È stato inoltre rimosso il file temporaneo errato:

```text
backend/app/.main.py
```

## Review dello sprint

Lo Sprint 1 ha raggiunto l'obiettivo previsto. Il backend supporta ora un flusso completo e testato per la gestione degli animali collegati ai clienti.

Non sono state implementate funzionalità fuori scope:

- Frontend.
- Dashboard.
- Promemoria.
- Pagamenti.
- WhatsApp.
- Statistiche.
- Report.
- Lista d'attesa.

## Prossimo passo

Il prossimo passo proposto è la pianificazione della foundation frontend. L'implementazione dovrà iniziare dopo una decisione esplicita su scope e struttura tecnica.
