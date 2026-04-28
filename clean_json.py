import json
import shutil
import os

filepath = 'pizzeria-piccola.json'
bakpath = 'pizzeria-piccola.json.bak'

# 1. Backup erstellen
if not os.path.exists(bakpath):
    shutil.copy(filepath, bakpath)
    print(f"Backup erstellt: {bakpath}")

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Unnötige Daten (Bloat) aus den Produkten entfernen, die für die Webseite nicht zwingend gebraucht werden
cleaned_count = 0
for pid, item in data.get('product', {}).items():
    # priceV2 wird eigentlich nur für den komplizierten alten Checkout verwendet,
    # generate.py braucht es nicht zwingend zum Anzeigen. options, img, stype sind leer
    # oder ungenutzt auf der reinen Speisekarte.
    keys_to_remove = ['priceV2', 'stype', 'img', 'options']
    for k in keys_to_remove:
        if k in item:
            del item[k]
            cleaned_count += 1
            
    # Leere Beschreibung wegräumen für mehr Übersicht, falls gewünscht
    # if 'desO' in item and str(item['desO']).strip() == "":
    #     del item['desO']

# 3. Datei ordentlich und kompakt formatiert (mit 4 Leerzeichen) abspeichern
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Fertig! Die Datei {filepath} wurde erfolgreich aufgeräumt und formatiert.")
print(f"Es wurden {cleaned_count} unnötige/leere Felder entfernt, sodass sie jetzt sehr viel übersichtlicher ist.")
