from util import img_util, settings
from ml import yolo, easy, tesseract

import argparse


def read_args():
    """
    Ließt die Kommandozeilen-Parameter ein

    Args:

    Returns:
        OCR-Servicewahl
        Frage, wie lange das Programm laufen soll
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file",
        dest="file",
        required=True,
        help="Bearbeitet das angegebene Bild",
        type=str
    )

    parser.add_argument(
        "-s", "--save",
        dest="save_path",
        help="Speichert alle Zwischenschritte der Bearbeitung in SAVE-PATH",
        type=str
    )

    parser.add_argument(
        "-o", "--ocr",
        choices=("easyocr", "tesseract"),
        dest="ocrservice",
        default="easyocr",
        help="Setzt den OCR-Service"
    )

    args = parser.parse_args()

    if args.save_path:
        settings.key_req.save_path = args.save_path
        settings.key_req.save_steps = True

    return args.ocrservice, args.file


def key_req(img, easyocr=True):
    """
    Führt die Texterkennung für einen Schlüssel aus

    Args:
        get_img: Parameterlose Funktion, die ein Bild liefert. Für dieses Bild wird die Texterkennung gestartet.
        easyocr: Benutzt EasyOCR für die Texterkennung
    """
    # NN initialisieren
    print("Initialisiere Schlüsselreidedetektion")
    print("-"*70)
    neuronal = yolo.nn()
    print("-"*70 + "\n\n")

    # Schlüssel ausschneiden
    img_cropped, _ = neuronal.crop_img(img)

    # OCR initialisieren
    if easyocr:
        print("Initialisiere OCR")
        print("-"*70)
        ocr = easy.ocr()
        print("-"*70 + "\n\n")

        text = img_util.text_rec_easy(img_cropped, ocr=ocr)

    else:
        text = img_util.text_rec(img_cropped)

    # Erkannten Text ausgeben
    print(text)


if __name__ == "__main__":
    ocr, file = read_args()
    img = img_util.open_img(file)
    key_req(img, easyocr=(ocr == "easyocr"))
