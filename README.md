# CO2 Emissions Analysis

Dieses Schulprojekt untersucht, wie gut sich jährliche CO2-Emissionen aus Bevölkerungs-, Wirtschafts- und Energiedaten abschätzen lassen. Als Quelle dient der öffentliche [Our World in Data CO2-Datensatz](https://github.com/owid/co2-data).

## Inhalt

- `data_description.ipynb`: Datenqualität, Kennzahlen und Verteilungen
- `model.ipynb`: ursprünglicher Modellvergleich der Abgabe
- `evaluation.ipynb`: ursprüngliche Auswertung und Visualisierungen
- `validate_model.py`: strengere, gruppierte Validierung auf unbekannten Ländern
- `data/co2_clean_1000.csv`: bereinigtes Demo-Sample mit 1'000 Zeilen

## Reproduzieren

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python validate_model.py
jupyter lab
```

## Methodik

Die ursprünglichen Notebooks verwenden einen zufälligen Zeilen-Split. Das ist für eine erste Schulabgabe verständlich, kann aber Informationen desselben Landes auf Training und Test verteilen. `validate_model.py` verwendet deshalb drei getrennte Mengen:

1. Training auf einer Gruppe von Ländern
2. Modellwahl auf anderen Ländern
3. einmalige Schlussbewertung auf vollständig unbekannten Ländern

Als Modelle werden eine lineare Regression und Entscheidungsbäume mit mehreren Tiefen verglichen. Bewertet wird mit MAE, RMSE und R².

## Grenzen

Das mitgelieferte Demo-Sample enthält nur 1'000 alphabetisch ausgewählte Zeilen und damit keine repräsentative Länderstichprobe. Die Resultate sind eine technische Demonstration und keine belastbare globale Emissionsprognose. Für eine wissenschaftliche Auswertung muss das Sample reproduzierbar aus einer festgehaltenen OWID-Version gezogen und zeitlich oder geografisch repräsentativ aufgebaut werden.

`energy_per_capita` stammt aus demselben Berichtsjahr wie der Zielwert. Das Projekt beschreibt daher Zusammenhänge und ist ohne klaren Prognosezeitpunkt noch kein Vorhersagesystem für zukünftige Emissionen.

## Daten und Lizenz

- Quelle: Our World in Data, `owid/co2-data`
- Datensatz-Lizenz: Die einzelnen Datenfelder können Bedingungen ihrer jeweiligen Originalquellen unterliegen. Für eine Weiterveröffentlichung müssen die Angaben im OWID-Codebook geprüft werden.
- Personenbezogene Daten: keine; die Zeilen beschreiben Länder und Jahre.
