# Arhitektura

Projekt je sestavljen iz dveh aplikacij: frontend je napisan v Vue 3, backend pa v FastAPI. Frontend sprejme uporabnikov vnos, backend izvede simulacije nad zgodovinskimi CSV-podatki in vrne primerjave ter povezave do grafov.

## Pregled sistema

```text
Uporabnik
   ↓
Vue frontend (localhost:3000)
   ↓  HTTP/JSON
FastAPI backend (localhost:8000)
   ↓
Izračuni in zgodovinski CSV-podatki
   ↓
Rezultati primerjave + HTML-grafi
   ↓
Frontend prikaže tabelo in graf v modalu
```

## Struktura repozitorija

```text
Leverage-Etfs/
├── frontend/               # Vue 3 uporabniški vmesnik
│   ├── src/
│   │   ├── main.ts         # zagon aplikacije in router
│   │   ├── App.vue         # skupni layout
│   │   └── views/          # posamezne strani
│   └── package.json
├── backend/                # FastAPI in izračuni
│   ├── main.py             # API in glavni potek
│   ├── izracuni.py         # finančni izračuni
│   ├── grafi.py            # izdelava grafov
│   ├── testing_file.py     # primerjava rezultatov
│   └── podatki*/           # vhodni CSV-podatki
├── docs/                   # ta dokumentacija
└── mkdocs.yml              # konfiguracija MkDocs
```

## Tok frontend aplikacije

```text
index.html
   ↓
src/main.ts
   ↓
src/App.vue
   ↓
RouterView
   ├── Home.vue
   ├── About.vue
   ├── Features.vue
   └── Contact.vue
```

`index.html` vsebuje element `#root`. `main.ts` ustvari Vue aplikacijo, priklopi router in jo namesti v ta element. `App.vue` prikazuje navigacijo, trenutno stran prek `RouterView` in footer.

## Tok simulacije

```text
Obrazec v Home.vue
   ↓
POST /primerjava_vrstic
   ↓
Povzetek in razvrščeni rezultati 1x, 2x in 3x
   ↓
POST /html-files
   ↓
Generiranje HTML-grafov
   ↓
Prikaz rezultatov in izbranega grafa
```

Klica se izvajata zaporedno. Frontend pričakuje, da je vrstni red grafov enak vrstnemu redu rezultatov primerjave.

## Ustvarjene datoteke

Backend med delovanjem uporablja oziroma ustvarja naslednje mape:

- `backend/testing/` za začasne rezultate simulacij;
- `backend/rezultati-vsak-interval-vsi-indeksi/` za podrobne rezultate;
- `backend/mapa-grafi/` za HTML-grafe, ki so dostopni prek `/grafi`.

Te mape so lokalni rezultat izvajanja in so izključene iz Gita.
