from pytest import fixture
from freifunk_website_proxy.proxy import Proxy


@fixture
def domain():
    """The domain name of the proxy"""
    return "proxy.freifunk.net"


@fixture
def proxy(domain):
    """A Proxy to test."""
    return Proxy(domain)
