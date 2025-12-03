import pandas as pd
from datetime import datetime, timedelta

# Dezember 2025 neu erstellen
year, month = 2025, 12

standorte = [
    'Delmenhorst', 'Güstrow', 'Döbeln', 'Melle', 'Langenfeld',
    'Kassel', 'Berlin', 'Aschaffenburg', 'Renningen'
]

# Generiere Werktage
start_date = datetime(year, month, 1)
end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
dates = pd.date_range(start=start_date, end=end_date, freq='D')
werktage = [d for d in dates if d.weekday() < 5]

# Erstelle Daten
data = []
for date in werktage:
    for standort in standorte:
        data.append({
            'Datum': date.strftime('%d.%m.%Y'),
            'Standort': standort,
            'Disponent': '',
            'Fahrzeuge': '',
            'Stopps': '',
            'Unverplante Stopps': '',
            'Kosten Fuhrpark': '',
            'Stoppschnitt': '',
            'Stoppkosten': ''
        })

df = pd.DataFrame(data)
df.to_csv('monatsdaten/2025-12.csv', sep=';', index=False)
print(f'Dezember 2025 neu erstellt!')
print(f'- {len(df)} Zeilen')
print(f'- {len(werktage)} Werktage')
print(f'- {len(standorte)} Standorte')
print()
print('Erste 10 Zeilen:')
print(df.head(10).to_string())
