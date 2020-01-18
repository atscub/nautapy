import re

from nautapy.exceptions import NautaFormatException

_re_time = re.compile(r'^\s*(?P<hours>\d+?)\s*:\s*(?P<minutes>\d+?)\s*:\s*(?P<seconds>\d+?)\s*$')


def strtime2seconds(str_time):
    res = _re_time.match(str_time)
    if not res:
        raise NautaFormatException("El formato del intervalo de tiempo es incorrecto: {}".format(str_time))

    return \
        int(res["hours"]) * 3600 + \
        int(res["minutes"]) * 60 + \
        int(res["seconds"])


def seconds2strtime(seconds):
    return "{:02d}:{:02d}:{:02d}".format(
        seconds // 3600,         # hours
        (seconds % 3600) // 60,  # minutes
        seconds % 60             # seconds
    )


def val_or_error(callback):
    try:
        return callback()
    except Exception as ex:
        return ex.args[0]