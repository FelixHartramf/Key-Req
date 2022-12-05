import torch
from util.settings import yolov5 as settings
from util import img_util


class nn:

    def __init__(self):
        """
        Initialisiert das Model mit einem voreingestellten Model
        """
        self.model = torch.hub.load(settings.repo, settings.model,
                                    path=settings.custom_model_path,
                                    force_reload=settings.force_reload, trust_repo=True)

    def crop_img(self, img, opencv=True):
        """
        Schneidet den Schlüssel aus einem Bild aus 

        Args:
            self
            img: Bild, aus dem ein Schlüssel ausgeschnitten wurde
            opencv: Gibt an, ob das Bild im OpenCV BGR-Format übergeben wird

        Returns:
            Bild des ausgeschnittenen Schlüssels
            Confidence, dass es ein Schlüssel ist
        """

        if opencv:
            # OpenCV verwendet BGR, wir brauchen aber RGB
            img_yolo = img[..., ::-1]
        else:
            img_yolo = img
        results = self.model(img_yolo)

        # ToDo Umgang bei mehreren erkannten Schlüsseln
        if len(results.pandas().xyxy[0]["confidence"].values) != 1:
            return img, 0

        confidence = results.pandas().xyxy[0]["confidence"].values[0]
        x_min = int(results.pandas().xyxy[0]["xmin"].values[0])
        x_max = int(results.pandas().xyxy[0]["xmax"].values[0])
        y_min = int(results.pandas().xyxy[0]["ymin"].values[0])
        y_max = int(results.pandas().xyxy[0]["ymax"].values[0])
        return img_util.crop(img, x_min, x_max, y_min, y_max), confidence


if __name__ == "__main__":
    pass
