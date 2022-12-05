import cv2
import numpy as np
from util.settings import key_req as settings
from ml import easy, tesseract


def resize(img, height=640):
    """
    Passt das Bild img so an, dass es height Pixel hoch ist

    Args:
        img: Bild, das angepasst werden soll
        height: neue Höhe des Bildes

    Returns:
        Angepasstes Bild
    """
    fac = height / img.shape[0]
    return cv2.resize(img, None, fx=fac, fy=fac)


def open_img(path, flag=cv2.IMREAD_ANYCOLOR):
    """
    Öffnet das Bild am Pfad path

    Args:
        path: Pfad des Bildes
        flag: Modus, in dem das Bild geöffnet werden soll

    Returns:
        Geöffnetes Bild
    """
    return cv2.imread(path, flag)


def grey_to_color(img):
    """
    Wandelt ein Graustufenbild in ein BGR-Bild um

    Args:
        img: Graustufenbild

    Returns:
        img mit drei Farbkanälen
    """
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def draw_box(img, x_min, x_max, y_min, y_max, thickness=2):
    """
    Zeichnet ein Rechteck um einen ausgewählten Bereich

    Args:
        img: Bild, in das das Rechteck gezeichnet werden soll
        x_min: Minimaler x-Wert des Rechtecks
        x_max: Maximaler x-Wert des Rechtecks
        y_min: Minimaler y-Wert des Rechtecks
        y_max: Maximaler y-Wert des Rechtecks
        thickness: Liniendicke

    Returns:
        Bild mit eingezeichnetem Rechteck
    """
    return cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (250, 0, 0), thickness)


def draw_rotated_box(img, p1, p2, p3, p4, thickness=2):
    """

    Zeichnet ein rotiertes Rechteck um einen ausgewählten Bereich

    Args:
        img: Bild, in das das Rechteck gezeichnet werden soll
        p1: Eckpunkt des Rechtecks
        p2: Eckpunkt des Rechtecks
        p3: Eckpunkt des Rechtecks
        p4: Eckpunkt des Rechtecks
        thickness: Liniendicke

    Returns:
        Bild mit eingezeichnetem Rechteck

    """
    l1 = cv2.line(img, p1, p2, (250, 0, 0), thickness=thickness)
    l2 = cv2.line(l1, p2, p3, (250, 0, 0), thickness=thickness)
    l3 = cv2.line(l2, p3, p4, (250, 0, 0), thickness=thickness)
    l4 = cv2.line(l3, p4, p1, (250, 0, 0), thickness=thickness)
    return l4


def crop(img, x_min, x_max, y_min, y_max):
    """
    Schneidet einen ausgewählten Bereich aus dem Bild aus 

    Args:
        img: Bild, in das das Rechteck gezeichnet werden soll
        x_min: Minimaler x-Wert des Ausschnitts
        x_max: Maximaler x-Wert des Ausschnitts
        y_min: Minimaler y-Wert des Ausschnitts
        y_max: Maximaler y-Wert des Ausschnitts

    Returns:
        Bildausschnitt
    """
    return img[y_min:y_max, x_min: x_max]


def save(img, path: str):
    """
    Speichert ein Bild

    Args:
        img: Bild, das gespeichert werden soll
        path: Pfad, an dem das Bild gespeichert werden soll
    """
    cv2.imwrite(path, img)


def show(img, name: str = "Key"):
    """
    Zeigt ein Bild an

    Args:
        img: Bild, das angezeigt werden soll
        name: Name des Bildes 
    """
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def add_border(img, width: int = 5, grey_value: int = 170):
    """
    Zeichnet einen Rand um das Bild

    Args:
        img: Graustufenbild, dem ein Rand hinzugefügt werden soll
        width: Breite des Rahmens
        grey_values: Helligkeitswert des Rahmens

    Returns:
        Bild mit Rand
    """
    return cv2.copyMakeBorder(img,
                              width, width, width, width,
                              cv2.BORDER_CONSTANT, value=(grey_value))


def text_rec(img, name: str = "image"):
    """
    Führt die Texterkennung mit Tesseract aus 

    Args:
        img: Bildausschnitt mit einem Text
        name: Name des Bildes

    Returns:
        Erkannter Text
    """
    img_original = img

    # Bild verkleinern
    img_smaller = resize(img, settings.max_height)

    img_small = img_smaller
    # Falls gewünscht, Teile vom Bild wegschneiden
    if settings.cut_from_cropp:
        x_min = int(img_smaller.shape[1] * (settings.cut_percent_left/100))
        x_max = img_smaller.shape[1] - \
            int(img_smaller.shape[1] * (settings.cut_percent_right/100))
        y_min = int(img_smaller.shape[0] * (settings.cut_percent_top/100))
        y_max = img_smaller.shape[0] - \
            int(img_smaller.shape[0] * (settings.cut_percent_bottom/100))

        img_smaller = crop(img_smaller, x_min, x_max, y_min, y_max)

    # Einen leichten Blur anwenden
    img_blur = cv2.bilateralFilter(img_smaller, 9, 75, 75)

    # In ein Graustuffenbild umwandeln
    img_grey = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

    # Binarisieren
    thresh, img_tresh = cv2.threshold(
        img_grey, 0, 255, cv2.THRESH_OTSU)

    img = add_border(add_border(img_tresh, grey_value=0), grey_value=255)

    # Pytesseract verwenden
    try:
        text, img_box = tesseract.req_text(img)
    except:
        # Im Fehlerfall nichts zurückgeben
        return "", img_original

    # Alle Zwischenschritte speichern, falls gewüsncht
    if settings.save_steps:
        save(img_small, f"{settings.save_path}/{name}1cropped.jpg")
        save(img_smaller, f"{settings.save_path}/{name}2cropped2.jpg")
        save(img_blur, f"{settings.save_path}/{name}3blur.jpg")
        save(img_grey, f"{settings.save_path}/{name}4grey.jpg")
        save(img_tresh, f"{settings.save_path}/{name}5tresh.jpg")
        save(img, f"{settings.save_path}/{name}6corner.jpg")
        save(img_box, f"{settings.save_path}/{name}7fullbox.jpg")

    return text


def text_rec_easy(img, name="image", ocr=easy.ocr()):
    """
    Führt die Texterkennung mit EasyOCR durch

    Args:
        img: Bildausschnitt mit einem Text
        name: Name des Bildes
        ocr: EasyOCR-Instanz

    Returns:
        Erkannter Text
    """
    img_original = np.copy(img)

    # Bild verkleinern
    img_smaller = resize(img, settings.max_height_easy)

    # Texterkennung
    text, img_box = ocr.req_text(img_smaller)

    # Alle Zwischenschritte speichern, falls gewüsncht
    if settings.save_steps:
        save(img_original, f"{settings.save_path}/{name}1cropped.jpg")
        save(img_box, f"{settings.save_path}/{name}2fullbox.jpg")

    return text
