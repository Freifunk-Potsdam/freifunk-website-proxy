"""
This module controls the nginx server.
"""

import subprocess
import tempfile

current_file = None
current_process = None

def configure_nginx(configuration):
    """Restart nginx with a certain configuration."""
    global current_file, current_process
    if current_file is not None:
        current_file.close()
    current_file = tempfile.NamedTemporaryFile(mode="w", suffix=".conf", prefix="nginx-")
    current_file.write(configuration)
    current_file.flush()
    subprocess.run(["nginx", "-t", "-c", current_file.name], check=True)
    if current_process:
        subprocess.run(["nginx", "-s", "quit", ], check=True)
        print("Waiting for nginx to quit.")
        try:
            current_process.wait(1)
        except subprocess.TimeoutExpired:
            print("ERROR: Could not stop running nginx.")
    current_process = subprocess.Popen(["nginx", "-c", current_file.name])


def nginx_is_available():
    """Return whether nginx is available."""
    return subprocess.run(["which", "nginx"], stdout=None).returncode == 0


__all__ = ["configure_nginx", "nginx_is_available"]

