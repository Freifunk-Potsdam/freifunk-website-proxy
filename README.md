



Configuration
-------------

- `DOMAIN` default `localhost`  
  This is the domain your servers serves from.
  If DOMAIN is "test.freifunk.net", new a hostname "chocolate" is prepended so the website is served under "chocolate.test.freifunk.net".
- `NETWORK` default `10.0.0.0/8`  
  This is the network address of the accepted services.
  I.e. Freifunk in Potsdam covers `10.22.0.0/16`.




Development
-----------


Run the server

    python3 -m freifunk_website_proxy

Build the server and run it 

    docker build --tag niccokunzmann/freifunk-website-proxy . && docker run -p "9000:80" -p "9001:9001" -e "DOMAIN=localhost:9000" -it --rm niccokunzmann/freifunk-website-proxy

Dann ist der Server auf http://localhost:9000 bzw http://localhost:9001 erreichbar.

Run the tests

    watch -n 0.5 pytest

