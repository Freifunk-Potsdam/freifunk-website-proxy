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
def configuration_directory(tmpdir):
    """The folder for the configuration files."""
    return tmpdir.dirpath()


@fixture
def proxy(domain, configuration_directory):
    """A Proxy to test."""
    from freifunk_website_proxy.proxy import Proxy
    return Proxy(domain, configuration_directory)


@fixture
def sub_domain():
    return "test"


@fixture
def server_address():
    """A fictive but possible server address."""
    return ("localhost", 9090)


@fixture
def configuration_file(configuration_directory):
    """A possible configuration file."""
    return os.path.join(configuration_directory, "test-config")


@fixture
def website(server_address, domain, sub_domain, configuration_file):
    """A website to serve."""
    from freifunk_website_proxy.proxy import Website
    return Website(server_address, domain, sub_domain, configuration_file)
