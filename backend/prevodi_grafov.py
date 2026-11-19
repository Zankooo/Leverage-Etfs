"""Besedila in prikaz števil za grafe; jezik ne vpliva na izračune."""

PREVODI_GRAFOV = {
    "sl": {
        "title": "Simulacija naložbe",
        "date": "Datum",
        "value": "Vrednost (log)",
        "strategies": ["Osnoven indeks", "Vzvod 2x", "Vzvod 3x"],
        "chart": "Graf {number}",
        "invested": "Skupaj investirano",
        "initial": "Začetna investicija",
        "monthly": "Mesečne investicije",
        "total": "Vse skupaj",
        "final": "Končne vrednosti",
        "date_format": "%d.%m.%Y",
        "separators": ",.",
    },
    "en": {
        "title": "Investment simulation",
        "date": "Date",
        "value": "Value (log)",
        "strategies": ["Unleveraged index", "2x leverage", "3x leverage"],
        "chart": "Chart {number}",
        "invested": "Total invested",
        "initial": "Initial investment",
        "monthly": "Monthly contributions",
        "total": "Total contributions",
        "final": "Final values",
        "date_format": "%m/%d/%Y",
        "separators": ".,",
    },
}


def prevodi_za_jezik(language="sl"):
    if language not in PREVODI_GRAFOV:
        raise ValueError("Jezik mora biti 'sl' ali 'en'.")
    return PREVODI_GRAFOV[language]


def plotly_config(language):
    """Prevodi orodne vrstice so vključeni v HTML, brez dodatnega CDN-ja."""
    prevodi_za_jezik(language)
    config = {"locale": language, "responsive": True, "displaylogo": False}
    if language == "sl":
        config["locales"] = {"sl": {
            "dictionary": {
                "Download plot as a PNG": "Prenesi graf kot PNG",
                "Zoom": "Povečava",
                "Pan": "Premakni",
                "Box Select": "Pravokotna izbira",
                "Lasso Select": "Prosta izbira",
                "Zoom in": "Povečaj",
                "Zoom out": "Pomanjšaj",
                "Autoscale": "Samodejno prilagodi osi",
                "Reset axes": "Ponastavi osi",
                "Toggle Spike Lines": "Preklopi vodilne črte",
                "Show closest data on hover": "Prikaži najbližje podatke",
                "Compare data on hover": "Primerjaj podatke",
                "Double-click to zoom back out": "Dvoklikni za ponastavitev povečave",
                "Double-click on legend to isolate one trace": "Dvoklikni legendo za prikaz samo ene serije",
                "Taking snapshot - this may take a few seconds": "Pripravljam sliko – to lahko traja nekaj sekund",
                "Snapshot succeeded": "Slika je pripravljena",
                "Sorry, there was a problem downloading your snapshot!": "Slike ni bilo mogoče prenesti.",
            },
            "format": {
                "decimal": ",", "thousands": ".", "date": "%d.%m.%Y",
                "days": ["nedelja", "ponedeljek", "torek", "sreda", "četrtek", "petek", "sobota"],
                "shortDays": ["ned", "pon", "tor", "sre", "čet", "pet", "sob"],
                "months": ["januar", "februar", "marec", "april", "maj", "junij", "julij", "avgust", "september", "oktober", "november", "december"],
                "shortMonths": ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "avg", "sep", "okt", "nov", "dec"],
            },
        }}
    return config
