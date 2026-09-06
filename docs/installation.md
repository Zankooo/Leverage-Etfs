# Namestitev in zagon

Za lokalni razvoj potrebuješ Python, Node.js in npm. Frontend, backend in dokumentacija tečejo kot trije ločeni procesi.

## 1. Backend

Iz korenske mape projekta ustvari Python virtualno okolje:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

Backend zaženi iz njegove mape, ker uporablja relativne poti do CSV-datotek:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Preveri delovanje na [http://localhost:8000](http://localhost:8000). Interaktivna FastAPI dokumentacija je na [http://localhost:8000/docs](http://localhost:8000/docs).

## 2. Frontend

V drugem terminalu zaženi:

```bash
cd frontend
npm install
npm run dev
```

Frontend je dostopen na [http://localhost:3000](http://localhost:3000).

## 3. Dokumentacija

V tretjem terminalu se vrni v korensko mapo projekta in zaženi:

```bash
mkdocs serve -a 127.0.0.1:8001
```

Dokumentacija je dostopna na [http://127.0.0.1:8001](http://127.0.0.1:8001). Uporablja port `8001`, ker backend že uporablja port `8000`.

## Preverjanje pred oddajo

Frontend preveri z ukazoma:

```bash
cd frontend
npm run lint
npm run build
```

Dokumentacijo preveri iz korenske mape:

```bash
mkdocs build --strict
```

## Windows

Aktivacija virtualnega okolja je na Windows drugačna:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r backend/requirements.txt
```

Ostali ukazi so enaki.
