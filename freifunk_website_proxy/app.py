import os
from bottle import run, route, static_file, redirect, post, request, re
from proxy import add_redirect

HERE = os.path.dirname(__file__ or ".")
STATIC_FILES = os.path.join(HERE, "static")
DOMAIN = os.environ.get("DOMAIN", "localhost")
MAXIMUM_HOST_NAME_LENGTH = 50

# ValidIpAddressRegex and ValidHostnameRegex from https://stackoverflow.com/a/106223
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"


@route("/")
def landing_page():
    """Redirect users from the landing page to the static files."""
    redirect("/static/")


@route("/static/<filename>")
@route("/static/")
def server_static(filename="index.html"):
    """Serve the static files."""
    return static_file(filename, root=STATIC_FILES)


@post("/add-page")
def add_server_redirect():
    """Add a new page to redirect to."""
    ip = request.forms.get("ip")
    hostname = request.forms.get("name")
    assert re.match(ValidHostnameRegex, hostname), "Hostname \"{}\" must match \"{}\"".format(hostname, ValidHostnameRegex)
    assert len(hostname) <= MAXIMUM_HOST_NAME_LENGTH, "The hostname \"{}\" must have maximum {} characters.".format(hostname, MAXIMUM_HOST_NAME_LENGTH)
    assert re.match(ValidIpAddressRegex, ip), "IP \"{}\" must match \"{}\"".format(ip, ValidIpAddressRegex)
    


def main():
    """Run the server app."""
    try:
        run(port=80, debug=True, host="")
    except PermissionError:
        pass
    else:
        return
    run(port=8080, debug=True, host="")

__all__ = ["main"]

