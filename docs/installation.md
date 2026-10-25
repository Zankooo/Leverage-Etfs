# Namestitev in zagon

Za lokalni razvoj potrebuješ Python 3 ter Node.js z npm. Izberi navodila za svoj operacijski sistem.

Backend in frontend tečeta v dveh ločenih terminalih. Dokumentacijo lahko po želji zaženeš v tretjem terminalu; za delovanje aplikacije ni potrebna.

Vsak terminal naj bo na začetku odprt v korenski mapi projekta `Leverage-Etfs`, kjer so mape `backend`, `frontend` in `docs`.

## macOS

### 1. Backend

V prvem terminalu ustvari in aktiviraj Python virtualno okolje ter namesti knjižnice:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

Nato se premakni v mapo `backend` in zaženi strežnik. Zagon iz te mape je pomemben, ker koda uporablja relativne poti:

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

Terminal pusti odprt. Backend je dostopen na [http://localhost:8000](http://localhost:8000).

### 2. Frontend

Odpri drugi terminal v korenski mapi projekta in zaženi:

```bash
cd frontend
npm install
npm run dev
```

Frontend je dostopen na [http://localhost:3000](http://localhost:3000).

### 3. Dokumentacija (neobvezno)

Odpri tretji terminal v korenski mapi projekta, aktiviraj isto virtualno okolje in namesti MkDocs s temo Material:

```bash
source .venv/bin/activate
python -m pip install mkdocs mkdocs-material
python -m mkdocs serve -a 127.0.0.1:8001
```

Dokumentacija je dostopna na [http://127.0.0.1:8001](http://127.0.0.1:8001).

### Ponovni zagon

Virtualno okolje in knjižnice namestiš ob prvi pripravi. Ob naslednjem zagonu backenda iz korenske mape uporabi:

```bash
source .venv/bin/activate
cd backend
python -m uvicorn main:app --reload --port 8000
```

Frontend ponovno zaženeš z `npm run dev` iz mape `frontend`.

## Windows (PowerShell)

### 1. Backend

V prvem terminalu ustvari virtualno okolje in namesti knjižnice:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Ukazi neposredno uporabljajo Python iz virtualnega okolja `.venv`, zato ga ni treba posebej aktivirati.

Nato se premakni v mapo `backend` in zaženi strežnik:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

Terminal pusti odprt. Backend je dostopen na [http://localhost:8000](http://localhost:8000).

### 2. Frontend

Odpri drugi terminal v korenski mapi projekta in zaženi:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Frontend je dostopen na [http://localhost:3000](http://localhost:3000).

### 3. Dokumentacija (neobvezno)

Odpri tretji terminal v korenski mapi projekta in zaženi:

```powershell
.\.venv\Scripts\python.exe -m pip install mkdocs mkdocs-material
.\.venv\Scripts\python.exe -m mkdocs serve -a 127.0.0.1:8001
```

Dokumentacija je dostopna na [http://127.0.0.1:8001](http://127.0.0.1:8001).

### Ponovni zagon

Virtualno okolje in knjižnice namestiš ob prvi pripravi. Ob naslednjem zagonu backenda iz korenske mape uporabi:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

Frontend ponovno zaženeš z `npm.cmd run dev` iz mape `frontend`.

## Lokalni naslovi in ustavitev

| Storitev | Naslov |
| --- | --- |
| Frontend | [http://localhost:3000](http://localhost:3000) |
| Backend | [http://localhost:8000](http://localhost:8000) |
| Interaktivna FastAPI dokumentacija | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Projektna dokumentacija | [http://127.0.0.1:8001](http://127.0.0.1:8001) |

Dokumentacija uporablja port `8001`, ker backend že uporablja port `8000`. Posamezen proces ustaviš s `Ctrl+C` v njegovem terminalu, tako na macOS kot na Windows.
