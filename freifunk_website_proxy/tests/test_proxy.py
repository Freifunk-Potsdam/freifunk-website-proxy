from pytest import mark
import os


def test_proxy_has_no_entries(proxy):
    assert len(proxy.websites) == 0


@mark.parametrize("sub_domain,port,host", [
    ("test", 8008, "localhost"),
    ("ffasd", 800, "quelltext.eu")])
def test_entry_is_listed(proxy, domain, sub_domain, port, host):
    proxy.serve((host, port), sub_domain)
    assert len(proxy.websites) == 1
    website = proxy.websites[0]
    assert website.host == host
    assert website.port == port
    assert website.domain == sub_domain + "." + domain


def test_proxy_has_no_configuration(proxy, configuration_directory):
    """Check that there is a configuration file which we can use."""
    assert os.path.exists(proxy.configuration_file)
    assert proxy.configuration_file.startswith(os.path.join(configuration_directory, ""))


@mark.parametrize("sub_domain,port,host", [
    ("test", 8008, "localhost"),
    ("ffasd", 800, "quelltext.eu")])
def test_entry_is_listed(proxy, domain, sub_domain, port, host, configuration_directory):
    proxy.serve((host, port), sub_domain)
    website = proxy.websites[0]
    assert website.configuration_file == os.path.join(configuration_directory, "websites", sub_domain)




