import os
from bottle import run, route, static_file, redirect, post, request, re, SimpleTemplate
from .proxy import Proxy
from .nginx import configure_nginx, nginx_is_available

HERE = os.path.dirname(__file__ or ".")
STATIC_FILES = os.path.join(HERE, "static")
DOMAIN = os.environ.get("DOMAIN", "localhost")
MAXIMUM_HOST_NAME_LENGTH = 50

# ValidIpAddressRegex and ValidHostnameRegex from https://stackoverflow.com/a/106223
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"


proxy = Proxy(DOMAIN)
def update_nginx():
    """Restart nginx with a new configuration."""
    print(proxy.get_nginx_configuration())
    if nginx_is_available():
        configure_nginx(proxy.get_nginx_configuration())
    else:
        print("NO NGINX")


@route("/")
def landing_page():
    """Redirect users from the landing page to the static files."""
    with open(os.path.join(HERE, "templates", "index.html")) as f:
        landing_page_template = SimpleTemplate(f.read())
    return landing_page_template.render(proxy=proxy)


@route("/static/<filename>")
def server_static(filename="index.html"):
    """Serve the static files."""
    return static_file(filename, root=STATIC_FILES)


@post("/add-page")
def add_server_redirect():
    """Add a new page to redirect to."""
    ip = request.forms.get("ip")
    port = request.forms.get("port")
    hostname = request.forms.get("name")
    assert re.match(ValidHostnameRegex, hostname), "Hostname \"{}\" must match \"{}\"".format(hostname, ValidHostnameRegex)
    assert len(hostname) <= MAXIMUM_HOST_NAME_LENGTH, "The hostname \"{}\" must have maximum {} characters.".format(hostname, MAXIMUM_HOST_NAME_LENGTH)
    assert re.match(ValidIpAddressRegex, ip), "IP \"{}\" must match \"{}\"".format(ip, ValidIpAddressRegex)
    assert port.isdigit(), "A port must be a number, not \"{}\".".format(port)
    port = int(port)
    assert 0 < port < 65536, "The port must be in range, not \"{}\".".format(port)
    website = proxy.serve((ip, port), hostname)
    update_nginx()
    redirect("/#" + website.id)


def main():
    """Run the server app."""
    update_nginx()
    run(port=9001, debug=True, host="")

__all__ = ["main"]

