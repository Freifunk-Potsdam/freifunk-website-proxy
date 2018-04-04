import os


def test_host_and_port_are_included(website, server_address):
    assert "{}:{}".format(*server_address) in website.get_nginx_configuration()


def test_domain_is_used(website, domain, sub_domain):
    assert "server_name {};".format(sub_domain + "." + domain) in website.get_nginx_configuration()


def test_website_does_not_write_to_file(website, configuration_file):
    assert not os.path.exists(configuration_file)


def test_website_can_write_configuration(website, configuration_file):
    website.write_nginx_configuration()
    assert os.path.exists(configuration_file)
    with open(configuration_file) as f:
        assert f.read() == website.get_nginx_configuration()
    
