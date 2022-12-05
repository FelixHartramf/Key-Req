# Key-Req
Key-Req ist ein Programm zur Identifikation von Schlüsseln aus Bilddateien.
Es wird der Ansatz der Texterkennung auf Schlüsseln (Schlüsselcodeerkennung) verfolgt.

## Installation
Zunächst muss das Project heruntergeladen 
und entpackt werden. Ein Wechsel in das Verzeichnis ist notwendig.
Es wird die Installation mit Docker empfohlen.

### Installation mit Docker
Das Docker-Image kann gebaut werden mit:
```
docker build -t felihart/key-req .
```
Dieser Vorgang kann ein paar Minuten dauern.
Es müssen mehrere Programme und Bibliotheken heruntergeladen werden.


Das Docker-Image kann interaktiv gestartet werden mit:
```
docker run -v $(pwd)/bilder:/bilder -a stdin -a stdout -i -t felihart/key-req /bin/bash
```
Nach dem ausführen des letzten Kommandos befindet man sich im gestarteten Docker Container und kann das Programm verwenden.

### Installation direkt auf dem System
Es wird  [Tesseract](https://pkgs.org/search/?q=tesseract-ocr) und [Python 3.10.5](https://www.python.org/downloads/release/python-3105/) oder höher benötigt.
Die benötigen Python-Bibliotheken werden installiert mit:
```
pip install -r /key-req/requirements.txt
```
Es wird die Verwendung einer virtuellen Pythonumgebung empfohlen.

## Verwendung des Programms 
Das Programm wird gestartet mit:
```
python key-req/key-req.py
```
Bei der ersten Ausführung werden noch weitere Dateien heruntergeladen.
Entsprechend dauert die erste Ausführung länger.

Bilder können in `bilder/` Abgelegt werden.
Soll also dieses bearbeitet werden, ist folgender Aufruf notwendig:
```
python key-req/key-req.py -f bilder/key.jpg
```
Um die einzelnen Bearbeitungsschritte nachvollziehen 
zu können, kann mit `-s SAVE_PATH` ein Ordner angegeben werden,
in dem die Bilder gespeichert werden:
```
python key-req/key-req.py -f bilder/key.jpg -s bilder
```

Es stehen folgende optionale Parameter zur Verfügung:
| Argument                 | Funktion                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `-h`                     | Anzeige des Hilfetextes                                                               |
| `-f FILE`                | Führt die Texterkennung für die die Datei `FILE` aus                                  |
| `-o {easyocr,tesseract}` | Setzt den OCR-Service entsprechend nach Angabe. Standardmäßig wird EasyOCR verwendet. |
| `-s SAVE-PATH`           | Speichert die Bilder während der Bearbeitung in dem Verzeichnis SAVE-PATH             |

Das Programm wurde nur für `.jpg` und `.png` Bilddateien getestet.





