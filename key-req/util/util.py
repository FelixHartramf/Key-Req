from util.settings import tesseract as settings


def remove_unwanted_chars(str1: str, whitelist: str = settings.whitelist) -> str:
    """
    Entfernt alle Zeichen, die in der Whitelist nicht aufgeführt sind 
    und gibt den neuen String zurück

    Args:
        str1: String aus dem alle nicht erlaubten Zeichen entfernt werden
        whitelist: String, der alle erlaubten Zeichen enthält

    Returns:
        str1, der nur aus Zeichen aus der Whitelist besteht
    """
    str_ret = ""
    for c in str1:
        if c in whitelist:
            str_ret += c
    return str_ret
