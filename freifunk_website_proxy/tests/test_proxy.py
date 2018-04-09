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


class TestServingWebsites:
    """Test serving mutiple websites"""

    def test_entries_with_same_domain_name_are_replaced_if_port_differs(self, proxy):
        website1 = proxy.serve(("10.22.254.111", 80), "test1")
        website2 = proxy.serve(("10.22.254.111", 81), "test1")
        assert not website1.is_served()
        assert website2.is_served()


    def test_entries_with_same_domain_name_are_replaced_if_ip_differs(self, proxy):
        website1 = proxy.serve(("10.22.254.111", 80), "test1")
        website2 = proxy.serve(("10.22.254.112", 80), "test1")
        assert not website1.is_served()
        assert website2.is_served()


    def test_entries_with_different_domain_name_are_not_replaced(self, proxy):
        website1 = proxy.serve(("10.22.254.111", 80), "test2")
        website2 = proxy.serve(("10.22.254.112", 80), "test1")
        assert website1.is_served()
        assert website2.is_served()

