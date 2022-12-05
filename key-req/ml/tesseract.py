import pytesseract
from util.settings import tesseract as settings
import cv2
from util import img_util


def req_text(img):
    """
    Texterkennung eines vorbereiteten Schlüssels 

    Args:
        img: Vorbearbeitete Datei

    Returns:
        text: Erkannter Text 
        img: Bearbeitetes Bild mit eingezeichneten Boxen um die erkannten Teile herum
    """

    config = f"--psm {settings.psm} --oem {settings.oem} -c tessedit_char_whitelist={settings.whitelist}"

    # Pytesseract anwenden
    output = pytesseract.image_to_data(
        img, timeout=settings.timeout, lang=settings.lang, config=config, output_type=pytesseract.Output.DICT)

    # Nur den Text mit der passenden minimalen Confidence nehmen
    text = ""
    for i in range(len(output["level"])):
        if float(output["conf"][i]) >= settings.min_conf:
            text += output["text"][i]

    # Boxen um die gefunden Texte anzuzeigen
    if settings.show_boxes:

        # Bild umwandeln für farbige Boxen
        img = img_util.grey_to_color(img)

        for i in range(len(output["level"])):
            if output["text"][i] != "" and float(output["conf"][i]) >= settings.min_conf:
                left = output["left"][i]
                top = output["top"][i]
                width = output["width"][i]
                height = output["height"][i]

                img_util.draw_box(img, left, left+width, top, top+height)

                if settings.show_text:
                    cv2.putText(img, f"{output['text'][i]} conf:{output['conf'][i]} ",
                                (left, top), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (250, 0, 0), 2)

    return text, img
