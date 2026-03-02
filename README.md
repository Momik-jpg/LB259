# LB259 – CO2-Datensatz 

## Datensatzbeschreibung
Für dieses Projekt nutze ich den Datensatz `owid-co2-data` von Our World in Data. Er enthält globale Klima- und Emissionswerte pro Land und Jahr und ist mit 50'411 Zeilen gross genug für belastbare Auswertungen. In diesem Repository liegt eine bereinigte Demo-Datei mit 1'000 Zeilen: `data/co2_clean_1000.csv`. Verwendet werden die Felder `country`, `iso_code`, `year`, `population`, `gdp`, `co2`, `energy_per_capita` und `methane`, weil sie gut zeigen, wie Wirtschaft, Energieverbrauch und Emissionen zusammenhängen.

## Datenschutz und Massnahmen
Der Datensatz enthält keine personenbezogenen Informationen, sondern nur aggregierte Werte auf Länder- und Jahresebene. Dadurch ist das direkte Datenschutzrisiko niedrig. Ein Restrisiko besteht nur, wenn solche Daten mit externen Mikrodaten kombiniert werden. Um das weiter zu reduzieren, habe ich nur nötige Spalten übernommen, keine IDs gespeichert und ausschliesslich aggregierte Variablen genutzt. Quelle und Lizenz sind unten dokumentiert, damit die Verwendung transparent und nachvollziehbar bleibt.

## Quelle und Lizenz
Quelle: Our World in Data – CO2 Data  
https://github.com/owid/co2-data

Lizenz: Creative Commons Attribution 4.0 International (CC BY 4.0)
