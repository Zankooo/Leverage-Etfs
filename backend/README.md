
# Navodila za namestitev in delovanje
## MacOS
Ustvari okolje:
```bash
python3 -m venv .venv
```
Aktiviraj okolje:
```bash
source .venv/bin/activate
```

Instaliraj knjiznice:
```bash
python -m pip install -r requirements.txt
```
Zaženi:
```bash
uvicorn main:app --reload
```

## Windows

Ustvari okolje:
```bash
python -m venv .venv
```
Aktiviraj okolje:
```bash
.venv\Scripts\activate
```

Instaliraj knjiznice:
```bash
python -m pip install -r requirements.txt
```
Zaženi:
```bash
uvicorn main:app --reload
```