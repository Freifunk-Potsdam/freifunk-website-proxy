







Development
-----------


Run the server

    python3 -m freifunk_website_proxy

Build the server and run it 

    docker build --tag niccokunzmann/freifunk-website-proxy . && docker run -it --rm niccokunzmann/freifunk-website-proxy

Run the tests

    watch -n 0.5 pytest
