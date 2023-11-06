import time
import csv  # Library für die Ausgabe in eine .csv Datei am Ende
import os   # Für das Öffnen von Excel durch das Terminal
from itertools import product   # Für das Erstellen der Liste von Kombinationen von True/False


def white(entry: list[bool]) -> (bool, bool):       # Methode für ein weißes Bauteil
    return tuple([not (entry[0] and entry[1])] * 2)


def red(entry: list[bool], orientation: list[str]) -> (bool, bool):     # Methode für einen roten Bausteil
    return tuple([not entry[orientation.index("R")]] * 2)


print("\nBWINF 2023: Aufgabe 4 (Nandu)\nLösung und Programm von Till Borckmann")
time.sleep(2)

# Datei einlesen
filename = "Example5"

with open(f"Examples/{filename}.txt", "r") as file:
    plaintext = file.read()

# Dateiinhalt wird in einzelne Zeilen aufgeteilt un in Array gespeichert (\n ist ein Zeilenumbruch)
content = plaintext.split("\n")
content.pop(0)  # Entfernen des ersten Elementes mit den Dimensionen des Steckbrettes

# Dateiinhalt an Leerzeichen aufteilen, um die einzelnen Bauteile zu erhalten
for i in range(len(content)):
    content[i] = content[i].split(" ")

# Entfernen aller leeren Strings aus dem Array
for i in range(len(content)):
    for j in range(content[i].count('')):
        content[i].remove('')

# Variable für das fertige Steckbrett wird beschrieben sowie ein Array für die Outputs der Bauteile einer Reihe wird erstellt
board: list[list[str]] = content

# Erstellt ein Array mit allen Inputs aus der Datei (Q1, Q2, ...)
inputsStrs = []
for part in board[0]:
    if part.startswith("Q"):
        inputsStrs.append(part)

# Erstellen eines Arrays für alle Kombinationen von True und False für spätere Schalttabelle
inputs = []
combinations = list(product([False, True], repeat=len(inputsStrs)))
for combination in combinations:
    inputs.append({inputsStrs[i]: combination[i] for i in range(len(inputsStrs))})

# Iteriert hier über alle möglichen Zustände der Eingänge
for index, input_combination in enumerate(inputs):

    # Es wird das Array output mit so vielen False gefüllt, wie die erste (bzw. jede) Zeile des Brettes lang ist.
    # Dadurch, dass die Variable hier überschrieben wird, wird verhindert, dass Ergebnisse aus der vorherigen Iteration die aktuelle beeinflussen
    output = [False] * len(board[0])

    # Eingänge werden gesucht und an der Stelle im Output mit dem gleichen Index dem passenden Zustand (an oder aus) entsprechend der aktuellen Kombination zugewiesen
    for i, char in enumerate(board[0]):
        if char.startswith("Q"):
            output[i] = input_combination[char]
    print("\nEingang: " + str(output))

    # Iteriert über alle Zeilen des Brettes, abgesehen von erster und letzter
    for i in range(1, len(board) - 1):  # ursprünglich mit for i in board[1: -1] versucht, ging aber nicht

        j = 0
        # Iteriert über alle Teile der Zeile des Brettes (while-Schleife, damit Index veränderbar ist)
        while j < len(board[i]):    # statt for j, part in enumerate(board[i]), hier Index aber nicht veränderbar
            part = board[i][j]
            # j - Index des aktuellen Bauteils
            # part - das aktuelle Bauteil

            # Wenn das Teil ein X (sprich leer) ist, wird Index erhöht und mit dem nächsten Teil fortgefahren
            if part == 'X':
                output[j] = False
                j += 1
                continue

            # Sonst wird, je nach Bauteil, die passende Funktion aufgerufen
            match part:     # match case ist äquivalent zu einer Verkettung von if-elif-else Abfragem, jedoch wesentlich übersichtlicher
                case "W":
                    output[j:j+2] = white(output[j:j+2])
                case "B":
                    pass    # wenn ein blaues Bauteil hier ist, wird der Output nicht verändert
                case "r":
                    output[j:j+2] = red(output[j:j+2], board[i][j:j+2])
                case "R":
                    # output[j], output[j+1] = red([output[j], output[j+1]], [board[i][j], board[i][j+1]]) - untere Zeile, aber ohne Slicing
                    output[j:j+2] = red(output[j:j+2], board[i][j:j+2])
            j += 2      # Index wird um 2 erhöht, da das Teil am nächsten Index das selbe Bauteil ist und somit bei einer Erhöhung des Index um nur 1 Fehler in der Berechnung auftreten würden
        print(output)

    # gibt letzte Zeile der Outputs aus
    print("Ausgang: " + str(output))
    # geht alle Bauteile in der letzten Zeile des Brettes durch
    for i, char in enumerate(board[-1]):
        # wenn das Bauteil eine LED ist (aka mit L beginnt), ...
        if char.startswith("L"):
            # ... wird diese LED mit dem zugehörigen Output dann in das Dictionary mit den Kombinationen aufgenommen
            inputs[index][char] = output[i]

# Die Ausgabe des Programmes in eine .csv Datei schreiben (mittels csv-Library)
with open("output.csv", "w") as file:
    file.write("sep=,\n")   # Fügt in die erste Zeile der Datei einen Vermerk auf den Seperator hinzu, damit in Excel die einzelnen Spalten voneinander getrennt sind
    writer = csv.DictWriter(file, inputs[0].keys())
    writer.writeheader()
    writer.writerows(inputs)
    print(f"\nDie Ausgabe wurde in die Datei {file.name} geschrieben!")

    # Angebot, die Ausgabedatei direkt in Excel zu öffnen
    if os.name == "nt" and input(f"Möchten Sie die Datei {file.name} in Excel öffnen? (y/n)\n   > ") == "y":
        os.system(f"start excel \"{file.name}\"")
        print("Datei wurde geöffnet!")
