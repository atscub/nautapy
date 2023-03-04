import os

import pytest
import requests
from requests_mock import Mocker as RequestMocker, ANY

from nautapy.exceptions import NautaLoginException, NautaPreLoginException
from nautapy.nauta_api import CHECK_PAGE, NautaProtocol


_assets_dir = os.path.join(
    os.path.dirname(__file__),
    "assets"
)


def read_asset(asset_name):
    with open(os.path.join(_assets_dir, asset_name)) as fp:
        return fp.read()


LANDING_HTML = read_asset("landing.html")
LOGIN_HTML = read_asset("login_page.html")
LOGGED_IN_HTML = read_asset("logged_in.html")


def test_nauta_protocol_creates_valid_session():
    with RequestMocker() as mock:
        # Setup
        mget = mock.get(ANY, status_code=200, text=LANDING_HTML)
        mpost = mock.post(ANY, status_code=200, text=LOGIN_HTML)

        # Test
        session, login_action, data = NautaProtocol.create_session()

        assert mget.called and mpost.called
        assert isinstance(session, requests.Session)
        assert login_action and data and data["CSRFHW"] and data["wlanuserip"]


def test_nauta_protocol_create_session_raises_when_connected():
    with RequestMocker() as mock:
        # Setup
        mget = mock.get(ANY, status_code=200, text="FOFOFOOFOFOFOFO")
        mpost = mock.post(ANY, status_code=200, text=LOGIN_HTML)

        with pytest.raises(NautaPreLoginException):
            NautaProtocol.create_session()

        assert mget.called and not mpost.called


def test_nauta_protocol_login_ok():
    with RequestMocker() as mock:
        mpost = mock.post(ANY, status_code=200, text=LOGGED_IN_HTML, url="http://secure.etecsa.net:8443/online.do?fooo")
        NautaProtocol.login(requests.Session(), "http://test.com/some_action", {}, "pepe@nauta.com.cu", "somepass")

