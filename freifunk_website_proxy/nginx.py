"""
This module controls the nginx server.
"""

import subprocess

current_file = None

def configure_nginx(configuration):
    """Restart nginx with a certain configuration."""
    global current_file
    if current_file is not None:
        current_file.close()
    current_file = tempfile.NamedTemporaryFile()
    f.write(configuration)
    f.flush()
    subprocess.run(["nginx", "-t", "-c", f.name], check=True)
    subprocess.run(["nginx", "-s", "reload", "-c", f.name], check=True)


def nginx_is_available(configuration):
    """Return whether nginx is available."""
    return subprocess.run(["which", "nginx"]).returncode == 0


__all__ = ["configure_nginx", "nginx_is_available"]

