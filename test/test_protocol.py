"""
Blackbox testing for the :class:`NautaProtocol` class

Usage:
    These test MUST be run locally with a private nauta account
    User credentials must be set in environment variables:
        $ export TEST_NAUTA_USERNAME="periquito@nauta.com.cu
        $ export TEST_NAUTA_PASSWORD="periquito_password"

    These test should be run independently with:
        pytest test/test_protocol.py

Description:
    The goal of these tests are to ensure that comunication
    with Nauta Captive Portal is not broken, maybe after an update.

    These tests must must not be run with the rest of the tests.
    Methods from :class:`NautaProtocol` must be mocked in all the
    other tests
"""

import os
import warnings

import pytest
from nautapy.nauta_api import NautaProtocol


def save_csrfhw(csrfhw):
    temp_dir = "temp"
    os.makedirs(temp_dir)
    with open(os.path.join("temp", "CSRFHW"), "w") as fp:
        fp.write(csrfhw)


def get_env_or_raise(env_var_name):
    env_var_val = os.getenv(env_var_name)
    if not env_var_val:
        raise Exception("{} is not defined in the environment".format(env_var_name))
    return env_var_val


@pytest.fixture()
def username():
    return get_env_or_raise("TEST_NAUTA_USERNAME")


@pytest.fixture()
def password():
    return get_env_or_raise("TEST_NAUTA_PASSWORD")


def test_nauta_protocol_logs_in(username, password):
    session, login_action, data = NautaProtocol.create_session()
    assert data and data["CSRFHW"]

    warnings.warn(
        "In case something went wrong, "
        "disconnect with this CSRFHW={}".format(
            data["CSRFHW"]
        )
    )

    attribute_uuid = None
    try:
        attribute_uuid = NautaProtocol.login(
            session=session,
            login_action=login_action,
            data=data,
            username=username,
            password="AnaD!az56"
        )

        if not attribute_uuid:
            warnings.warn("attribute_uuid was not found after login")
    finally:
        NautaProtocol.logout(
            csrfhw=data["CSRFHW"],
            username=username,
            wlanuserip=data["wlanuserip"],
            attribute_uuid=attribute_uuid
        )


# _assets_dir = os.path.join(
#     os.path.dirname(__file__),
#     "assets"
# )
#
#
# def read_asset(asset_name):
#     with open(os.path.join(_assets_dir, asset_name)) as fp:
#         return fp.read()
#
#
# LANDING_HTML = read_asset("landing.html")
# LOGIN_HTML = read_asset("login_page.html")
# LOGGED_IN_HTML = read_asset("logged_in.html")
#
#
# def test_nauta_protocol_creates_valiad_session():
#     with RequestMocker() as mock:
#         # Setup
#         mget = mock.get(ANY, status_code=200, text=LANDING_HTML)
#         mpost = mock.post(ANY, status_code=200, text=LOGIN_HTML)
#
#         # Test
#         session, login_action, data = NautaProtocol.create_session()
#
#         assert mget.called and mpost.called
#         assert isinstance(session, requests.Session)
#         assert login_action and data and data["CSRFHW"] and data["wlanuserip"]
#
#
# def test_nauta_protocol_create_session_raises_when_connected():
#     with RequestMocker() as mock:
#         # Setup
#         mget = mock.get(ANY, status_code=200, text="FOFOFOOFOFOFOFO")
#         mpost = mock.post(ANY, status_code=200, text=LOGIN_HTML)
#
#         with pytest.raises(NautaPreLoginException):
#             NautaProtocol.create_session()
#
#         assert mget.called and not mpost.called
#
#
# def test_nauta_protocol_login_ok():
#     with RequestMocker() as mock:
#         mpost = mock.post(ANY, status_code=200, text=LOGGED_IN_HTML, url="http://secure.etecsa.net:8443/online.do?fooo")
#         NautaProtocol.login(requests.Session(), "http://test.com/some_action", {}, "pepe@nauta.com.cu", "somepass")
#
