"""
This module is the interface to the http proxy.

"""
import os

PROXY_PARAMS = """
roxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header User-Agent $http_user_agent;

client_max_body_size 100M;
client_body_buffer_size 1m;
proxy_intercept_errors on;
proxy_buffering on;
proxy_buffer_size 128k;
proxy_buffers 256 16k;
proxy_busy_buffers_size 256k;
proxy_temp_file_write_size 256k;
proxy_max_temp_file_size 0;
proxy_read_timeout 300;
"""

class Website:
    """This is a website entered by the proxy."""
    
    configuration_template = """
    server {{
        server_name {domain};

        listen   0.0.0.0:80;

        access_log off;

        location / {{
            """ + PROXY_PARAMS + """
            proxy_pass http://{host}:{port};
        }}
    }}
    """

    def __init__(self, server_address, domain, sub_domain, configuration_file):
        """Create a new website."""
        self.host, self.port = server_address
        self.domain = sub_domain + "." + domain
        self.configuration_file = configuration_file
        self.id = self.domain
        
    def get_nginx_configuration(self):
        """Return the nginx configuration for the website to serve"""
        return self.configuration_template.format(host=self.host, port=self.port, domain=self.domain)
    
    def write_nginx_configuration(self):
        with open(self.configuration_file, "w") as f:
            f.write(self.get_nginx_configuration())


class Proxy:
    """Create a proxy class for a given domain name"""

    def __init__(self, domain, configuration_directory):
        """Create a new Proxy.
        
        - domain is the domain name of the service. New entries will be sub-entries of this.
        """
        self.domain = domain
        self.websites = []
        self.configuration_directory = configuration_directory
        self.configuration_file = os.path.join(configuration_directory, "all")
        self.website_files = os.path.join(configuration_directory, "websites")
        os.makedirs(self.website_files, exist_ok=True)
        with open(self.configuration_file, "w"): pass

    def serve(self, server_address, sub_domain):
        """Serve the content from the server address at the sub_domain.
        
        - server_address - a tuple of (ip, port)
        - sub_domain - a valid domain name
        """
        configuration_file = os.path.join(self.website_files, sub_domain)
        website = Website(server_address, self.domain, sub_domain, configuration_file)
        self. websites.append(website)
        return website



