# Sprint 2 - Frontend Client Detail

## Stato

**DA INIZIARE**

## Obiettivo

Implementare il dettaglio cliente e la visualizzazione degli animali associati.

Flusso:

```text
Elenco clienti
    ↓
Apertura cliente
    ↓
Dettaglio cliente
    ↓
Lista animali associati
```

## Prima milestone

Dalla lista clienti l’utente deve poter:

- aprire un cliente;
- vedere i dati del cliente;
- vedere gli animali associati;
- vedere uno stato vuoto per un cliente senza animali;
- tornare alla lista.

Gestire loading, errori, cliente inesistente e valori opzionali mancanti.

## Scope incluso

Aggiungere preferibilmente:

```text
frontend/app/clients/[clientId]/page.tsx
```

Utilizzare gli endpoint esistenti:

```text
GET /clients/{client_id}
GET /clients/{client_id}/animals
```

Aggiungere o estendere il client API frontend senza duplicare codice già presente.

La pagina deve mostrare:

- nome e cognome;
- telefono;
- email;
- note;
- lista animali;
- specie;
- razza;
- taglia;
- età;
- note dell’animale;
- `—` per i valori mancanti;
- link per tornare all’elenco.

Aggiungere nella lista clienti un link `Visualizza` o `Dettagli`, senza rimuovere modifica ed eliminazione.

## Scope escluso

Non implementare nella prima milestone:

- creazione, modifica o eliminazione animali;
- appuntamenti;
- calendario;
- promemoria;
- dashboard;
- autenticazione;
- pagamenti;
- WhatsApp;
- statistiche;
- nuove librerie non necessarie;
- modifiche backend o database.

## File da analizzare

```text
frontend/app/page.tsx
frontend/app/layout.tsx
frontend/app/providers.tsx
frontend/components/clients/clients-page.tsx
frontend/components/clients/client-form.tsx
frontend/lib/api/clients.ts
frontend/package.json
```

Prima di modificare codice verificare routing, TanStack Query, risposte API, tipi, gestione errori e URL base.

## Ambiente locale

```bash
docker compose up -d

cd backend
uv run alembic upgrade head
uv run uvicorn app.main:app --reload

cd ../frontend
npm install
npm run dev
```

URL:

```text
Frontend: http://localhost:3000
Backend: http://127.0.0.1:8000
```

Verifiche:

```bash
curl -i http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/clients | python3 -m json.tool
```

Non rilanciare il seed senza controllare il database, per evitare duplicati.

## Sequenza di lavoro

1. Analizzare i file esistenti.
2. Proporre file, route, query e stati.
3. Attendere conferma per decisioni architetturali.
4. Implementare solo la prima milestone.
5. Eseguire:

```bash
cd frontend
npm run lint
npm run build
```

6. Testare dal browser:
   - cliente con un animale;
   - cliente con più animali;
   - cliente senza animali;
   - valori opzionali mancanti;
   - ID inesistente;
   - ritorno alla lista;
   - assenza di regressioni nella gestione clienti.
7. Aggiornare questo documento.
8. Aggiornare `docs/PROJECT_STATUS.md` dopo la verifica.
9. Creare un commit dedicato.

## Criteri di accettazione

- La lista clienti continua a funzionare.
- Ogni cliente ha un link al dettaglio.
- La route dinamica legge l’ID.
- I dati cliente arrivano dal backend.
- Gli animali arrivano dal backend.
- Il cliente senza animali ha uno stato vuoto chiaro.
- Il cliente inesistente ha un errore comprensibile.
- Loading ed errori sono gestiti.
- I dati opzionali mancanti sono visualizzati coerentemente.
- `npm run lint` passa.
- `npm run build` passa.
- I test manuali passano.
- La documentazione è aggiornata.