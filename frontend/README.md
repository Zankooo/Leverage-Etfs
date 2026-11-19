# Navodila za namestitev in delovanje
## MacOS in Windows
Instaliraj node_modules
```bash
npm install
```
Zaženi
```bash
npm run dev
```

## Jeziki

Frontend uporablja Vue I18n. Preklopnik **SL / EN** je v navigaciji tudi na
telefonu. Privzeti jezik je slovenščina; izbira se shrani v `localStorage`
pod ključem `vzvodno-language`.

Besedila urejaj v `src/locales/sl.ts` in `src/locales/en.ts`; obe datoteki
morata imeti enake ključe. V komponentah uporabljaj `t('home.calculate')`,
za številke `n(vrednost, 'decimal')`, za datume pa `d(datum, 'short')`.
Nastavitve, zapis izbire ter jezik in naslov dokumenta so v `src/i18n.ts`.

Preklop jezika ohrani vnose in prikazane rezultate simulacije. Vsebino grafov
v okvirju `iframe` še vedno pripravi backend v svojem obstoječem jeziku.


```mermaid
flowchart TD
    A[index.html] --> B[main.ts]
    B --> C[App.vue]
    C --> D[RouterView]
    D --> E[Home.vue]
    D --> F[About.vue]
    D --> G[Features.vue]
    D --> H[Contact.vue]
```
