import os
import sys
import json
import subprocess
from jinja2 import Environment, FileSystemLoader

# Functie om een server toe te voegen aan de lijst
def voeg_server_toe(server_lijst, naam, adres):
    server_lijst[naam] = adres
    opslaan_server_lijst(server_lijst)

# Functie om een server te verwijderen uit de lijst
def verwijder_server(server_lijst, naam):
    if naam in server_lijst:
        del server_lijst[naam]
        opslaan_server_lijst(server_lijst)
    else:
        print(f"Server met naam '{naam}' bestaat niet in de lijst.")

# Functie om de serverlijst op te slaan als JSON
def opslaan_server_lijst(server_lijst):
    with open('servers.json', 'w') as bestand:
        json.dump(server_lijst, bestand)

# Functie om de serverlijst te laden uit JSON
def laad_server_lijst():
    if os.path.exists('servers.json'):
        with open('servers.json', 'r') as bestand:
            return json.load(bestand)
    else:
        return {}

# Functie om een ping naar een server uit te voeren
def voer_ping_uit(server_naam, server_adres):
    try:
        resultaat = subprocess.check_output(['ping', '-c', '1', server_adres])
        return resultaat.decode('utf-8')
    except subprocess.CalledProcessError:
        return f"Kan de server '{server_naam}' niet pingen."

# Functie om rapporten te genereren
def genereer_rapport(server_lijst):
    template_env = Environment(loader=FileSystemLoader('.'))
    template = template_env.get_template('basis.html')
    rapport_data = []

    for naam, adres in server_lijst.items():
        ping_resultaat = voer_ping_uit(naam, adres)
        rapport_data.append({'naam': naam, 'adres': adres, 'ping_resultaat': ping_resultaat})

    rapport_html = template.render(rapport_data=rapport_data)
    with open('rapport.html', 'w') as bestand:
        bestand.write(rapport_html)

# Functie om het programma in management modus uit te voeren
def management_modus():
    server_lijst = laad_server_lijst()
    while True:
        print("1. Voeg een server toe")
        print("2. Verwijder een server")
        print("3. Toon de serverlijst")
        print("4. Exit")

        keuze = input("Kies een optie: ")

        if keuze == '1':
            naam = input("Voer de naam van de server in: ")
            adres = input("Voer het IP-adres of hostname in: ")
            voeg_server_toe(server_lijst, naam, adres)
        elif keuze == '2':
            naam = input("Voer de naam van de server in: ")
            verwijder_server(server_lijst, naam)
        elif keuze == '3':
            print("Serverlijst:")
            for naam, adres in server_lijst.items():
                print(f"{naam}: {adres}")
        elif keuze == '4':
            break

# Functie om het programma in check modus uit te voeren
def check_modus():
    server_lijst = laad_server_lijst()
    genereer_rapport(server_lijst)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        modus = sys.argv[1]
        if modus == 'management':
            management_modus()
        elif modus == 'check':
            check_modus()
        else:
            print("Ongeldige modus. Gebruik 'management' of 'check'.")
    else:
        print("Gebruik: python programma.py <modus>")
