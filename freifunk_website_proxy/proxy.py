"""
This module is the interface to the http proxy.

"""

class Proxy:
    """Create a proxy class for a given domain name"""

    def __init__(self, domain):
        """Create a new Proxy.
        
        - domain is the domain name of the service. New entries will be sub-entries of this.
        """
        self.domain = domain

    def serve(self, server_address, sub_domain):
        """Serve the content from the server address at the sub_domain.
        
        - server_address - a tuple of (ip, port)
        - sub_domain - a valid domain name
        """


