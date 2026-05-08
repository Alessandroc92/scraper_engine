from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os


def custom_namer(filename):
    basename = os.path.basename(filename)
    sp = basename.split(".")
    new_basename = f"{sp[0]}_{sp[-1]}.{sp[1]}"
    return filename.replace(basename, new_basename)


class CustomTimeRotatingHandler(TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.namer = custom_namer


class CustomFileRotatingHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            self.namer = custom_namer
        except FileNotFoundError:
            raise FileNotFoundError(
                'You need to create a folder name "logs" in your main directory.')
