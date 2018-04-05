







Development
-----------


Run the server

    python3 -m freifunk_website_proxy

Build the server and run it 

    docker build --tag niccokunzmann/freifunk-website-proxy . && docker run -p "9000:80" -p "9001:9001" -e "DOMAIN=localhost:9000" -it --rm niccokunzmann/freifunk-website-proxy

Dann ist der Server auf http://localhost:9000 bzw http://localhost:9001 erreichbar.

Run the tests

    watch -n 0.5 pytest

