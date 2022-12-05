import easyocr
from util import img_util, util
import cv2
from util.settings import tesseract as settings


class ocr:
    def __init__(self):
        """
        Initialisiert eine EasyOCR Instanz
        """

        self.reader = easyocr.Reader(['en'])

    def req_text(self, img):
        """
        Führt die Texterkennung für ein Bild aus 

        Args:
            img: Bildausschnitt mit Schlüsselreide

        Returns:
            Erkannter Text, bearbeitetes Bild
        """

        # Texterkennung ausführen
        output = self.reader.readtext(img)
        text = ""

        # Text zusammensetzen und Boxen um den Text einzeichnen
        for line in output:
            current_text = line[1]
            points = line[0]
            conf = line[2]

            text += current_text

            for i, point in enumerate(points):
                points[i] = int(point[0]), int(point[1])

            # Boxen um den erkannten Text einzeichnen
            if settings.show_boxes:

                img_util.draw_rotated_box(
                    img, points[0], points[1], points[2], points[3])

                cv2.putText(img, f"{current_text} conf:{conf} ",
                            (points[0]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (250, 0, 0), 2)

        text = util.remove_unwanted_chars(text)
        return text, img
