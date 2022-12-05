class key_req:
    """
    Klasse für die allgemeinen Einstellungen
    """
    save_steps = False

    max_height = 640
    max_height_easy = 960

    cut_from_cropp = True
    cut_percent_top = 20
    cut_percent_left = 10
    cut_percent_right = 20
    cut_percent_bottom = 5

    save_path = "./bilder-bearbeitet"


class tesseract:
    """
    Klasse für die Einstellungen von Tesseract
    """

    psm = "11"
    oem = "1"
    whitelist = ".ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    lang = "eng"
    timeout = 0.5
    min_conf = 15.0
    show_boxes = True
    show_text = True


class yolov5:
    """
    Klasse für die Einstellungen von Yolov5
    """

    load_at_start = True
    force_reload = False
    repo = "ultralytics/yolov5"
    model = "custom"
    custom_model_path = "key-req/models/reitev5.pt"
    max_res = 0
