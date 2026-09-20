# Frontend

Frontend je enostranska aplikacija, zgrajena z Vue 3, TypeScriptom, Vue Routerjem, Axiosom, Tailwind CSS in Vite.

## Pomembne datoteke

| Datoteka | Namen |
| --- | --- |
| `frontend/index.html` | Osnovni HTML in element `#root` |
| `frontend/src/main.ts` | Ustvari Vue aplikacijo in router |
| `frontend/src/App.vue` | Navigacija, prostor za stran in footer |
| `frontend/src/views/Home.vue` | Obrazec, API-klici in rezultati simulacije |
| `frontend/src/views/About.vue` | Predstavitev projekta |
| `frontend/src/views/Features.vue` | Prednosti aplikacije |
| `frontend/src/views/Contact.vue` | Kontaktni obrazec |
| `frontend/src/index.css` | Globalni CSS, Tailwind in pisava Inter |

## Routing

Router je definiran v `src/main.ts`:

| Pot | Komponenta | Stran |
| --- | --- | --- |
| `/` | `Home.vue` | Simulacija |
| `/about` | `About.vue` | O projektu |
| `/features` | `Features.vue` | Prednosti |
| `/contact` | `Contact.vue` | Kontakt |

`App.vue` uporablja `RouterView`, v katerega se vstavi komponenta trenutne poti.

## Stanje simulacije

`Home.vue` uporablja Vue `ref` za reaktivno stanje:

- `initialInvestment` – začetna investicija;
- `monthlyContribution` – mesečni vložek;
- `selectedIndex` – izbrani indeks;
- `selectedInterval` – dolžina obdobja;
- `isLoading` – stanje izvajanja zahtev;
- `tableRows` in `tableSummary` – rezultati primerjave;
- `results` – seznam ustvarjenih grafov;
- `showGraphModal` in `selectedGraphUrl` – stanje modalnega okna.

`computed` se uporablja za preverjanje obrazca in izračun skupnega vloženega zneska.

## API-komunikacija

Ob kliku na gumb **Izračunaj** funkcija `izracunaj()` pripravi podatke:

```json
{
  "zacetna_investicija": 1000,
  "mesecni_vlozek": 100,
  "indeks": "S&P 500",
  "interval": 15
}
```

Nato zaporedno pokliče:

1. `POST http://localhost:8000/primerjava_vrstic`;
2. `POST http://localhost:8000/html-files`.

Prvi odgovor napolni povzetek in vrstice rezultatov. Drugi odgovor vsebuje URL-je HTML-grafov. Izbrani graf se prikaže v elementu `iframe` znotraj modalnega okna.

## Slogi

Večina oblikovanja uporablja Tailwind utility razrede neposredno v Vue predlogah. `src/index.css` vsebuje globalni uvoz Tailwinda in pisave, komponenti `App.vue` in `Home.vue` pa vsebujeta še lasten CSS.

## Trenutne omejitve

- API-naslov je neposredno zapisan kot `http://localhost:8000`.
- Tipi odgovorov uporabljajo `any` namesto TypeScript vmesnikov.
- Večina logike in prikaza je združena v veliki komponenti `Home.vue`.
- Kontaktni obrazec še nima funkcije za pošiljanje.
- Povezava med vrstico rezultata in grafom temelji na istem indeksu v dveh seznamih.

Ob večji širitvi aplikacije je smiselno dodati mape `components/`, `services/` in `types/`.
