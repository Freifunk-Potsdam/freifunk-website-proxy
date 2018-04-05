"""
This module is the interface to the http proxy.

"""
import os

NGINX_CONFIGURATION = """
#
# copied from https://gist.githubusercontent.com/nishantmodak/d08aae033775cb1a0f8a/raw/ebea0ae66e0a0188009accae2acba88cc646ddcd/nginx.conf.default
#


#user  nobody;
#Defines which Linux system user will own and run the Nginx server

worker_processes  2;
#Referes to single threaded process. Generally set to be equal to the number of CPUs or cores.

#error_log  logs/error.log; #error_log  logs/error.log  notice;
#Specifies the file where server logs.

#pid        logs/nginx.pid;
#nginx will write its master process ID(PID).

events {{
    worker_connections  1024;
    # worker_processes and worker_connections allows you to calculate maxclients value:
    # max_clients = worker_processes * worker_connections
}}


http {{
    include       mime.types;
    # anything written in /opt/nginx/conf/mime.types is interpreted as if written inside the http block

    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $http_host $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    # If serving locally stored static files, sendfile is essential to speed up the server,
    # But if using as reverse proxy one can deactivate it

    #tcp_nopush     on;
    # works opposite to tcp_nodelay. Instead of optimizing delays, it optimizes the amount of data sent at once.

    #keepalive_timeout  0;
    keepalive_timeout  65;
    # timeout during which a keep-alive client connection will stay open.

    gzip  on;
    # tells the server to use on-the-fly gzip compression.

    {websites}
}}
"""

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

    def __init__(self, server_address, domain, sub_domain):
        """Create a new website."""
        self.host, self.port = server_address
        self.domain = sub_domain + "." + domain
        self.id = self.domain
        
    def get_nginx_configuration(self):
        """Return the nginx configuration for the website to serve"""
        return self.configuration_template.format(host=self.host, port=self.port, domain=self.domain)


class Proxy:
    """Create a proxy class for a given domain name"""

    def __init__(self, domain):
        """Create a new Proxy.
        
        - domain is the domain name of the service. New entries will be sub-entries of this.
        """
        self.domain = domain
        self.websites = []

    def serve(self, server_address, sub_domain):
        """Serve the content from the server address at the sub_domain.
        
        - server_address - a tuple of (ip, port)
        - sub_domain - a valid domain name
        """
        website = Website(server_address, self.domain, sub_domain)
        self. websites.append(website)
        return website
    
    def get_nginx_configuration(self):
        """Get the nginx configuration."""
        websites = [website.get_nginx_configuration() for website in self.websites]
        return NGINX_CONFIGURATION.format(websites="\n".join(websites))
            



