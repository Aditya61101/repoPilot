import os

from constants import EXTENSION_MAPPING

def detect_language(path):
    ext = os.path.splitext(path)[1].lower()

    return EXTENSION_MAPPING.get(ext, "generic")