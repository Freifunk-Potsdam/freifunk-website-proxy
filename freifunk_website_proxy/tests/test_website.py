import os


def test_host_and_port_are_included(website, server_address):
    assert "{}:{}".format(*server_address) in website.get_nginx_configuration()


def test_domain_is_used(website, domain, sub_domain):
    assert "server_name {};".format(sub_domain + "." + domain) in website.get_nginx_configuration()


