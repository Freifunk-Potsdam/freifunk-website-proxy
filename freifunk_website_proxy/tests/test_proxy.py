from pytest import mark
import os


def test_proxy_has_no_entries(proxy):
    assert len(proxy.websites) == 0


entries = mark.parametrize("sub_domain,port,host", [
    ("test", 8008, "localhost"),
    ("ffasd", 800, "quelltext.eu")])

@entries
def test_website_has_attributes(proxy, domain, sub_domain, port, host):
    proxy.serve((host, port), sub_domain)
    assert len(proxy.websites) == 1
    website = proxy.websites[0]
    assert website.host == host
    assert website.port == port
    assert website.domain == sub_domain + "." + domain


@entries
def test_proxy_updates(proxy, domain, sub_domain, port, host):
    website = proxy.serve((host, port), sub_domain)
    assert website.get_nginx_configuration() in proxy.get_nginx_configuration()
    


