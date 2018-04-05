from pytest import fixture
import os
import sys

HERE = os.path.dirname(__file__ or ".")
sys.path.append(os.path.join(HERE, "..", ".."))


@fixture
def domain():
    """The domain name of the proxy"""
    return "proxy.freifunk.net"


@fixture
def proxy(domain):
    """A Proxy to test."""
    from freifunk_website_proxy.proxy import Proxy
    return Proxy(domain)


@fixture
def sub_domain():
    return "test"


@fixture
def server_address():
    """A fictive but possible server address."""
    return ("localhost", 9090)


@fixture
def website(server_address, domain, sub_domain):
    """A website to serve."""
    from freifunk_website_proxy.proxy import Website
    return Website(server_address, domain, sub_domain)
