from nautacli.exceptions import NautaFormatException
from nautacli.utils import strtime2seconds, seconds2strtime
import pytest


@pytest.mark.parametrize("strtime, seconds", [
    ("01:00:00", 3600),
    (" 01:00 :30 ", 3630),
    (" 01: 05 :00 ", 3900),
    (" 50:00 :00 ", 50 * 3600),
])
def test_strtime2seconds(strtime, seconds):
    assert strtime2seconds(strtime) == seconds


@pytest.mark.parametrize("bad_formated", [
    ("10:00",),
    ("10",),
    ("a:00:00",),
    ("10:00::00",),
])
def test_strtime2seconds_raises_format_exception(bad_formated):
    with pytest.raises(NautaFormatException):
        strtime2seconds("")


@pytest.mark.parametrize("strtime, seconds", [
    ("01:00:00", 3600),
    ("01:00:30", 3630),
    ("01:05:00", 3900),
    ("50:00:00", 50 * 3600),
])
def test_seconds2strtime(strtime, seconds):
    assert seconds2strtime(seconds) == strtime

