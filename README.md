Freifunk Website Proxy
======================

[![Build Status](https://travis-ci.org/niccokunzmann/freifunk-website-proxy.svg?branch=master)](https://travis-ci.org/niccokunzmann/freifunk-website-proxy)
![Docker Build Status](https://img.shields.io/docker/build/niccokunzmann/freifunk-website-proxy.svg)

This is a tool to make local services served in a community network available to the outside internet.
The intention is to
1. lower the bar to create internet services
2. increase accessibility from inside and outside the community network and thus make services in the network more attractive

Using the Server
----------------

You create an http service in the local community network.
Then, you go to the website of your community. There may be many.
- [Potsdam][ffp]

You put in your ip address, your server name and your port.
When you submit, your website should be available under the hostname you entered.

Setting up a Server
-------------------

You can setup the server for your community in case the server is not there.
1. Install [docker](https://docs.docker.com/install)b.
   You will need a 64 bit computer.
   ```
   wget -O- https://get.docker.com | sh
   ```
2. Start the server replacing the configuration variables accordingly.
   ```
   docker run -p "80:80" -e "DOMAIN=MY-DOMAIN" -d --rm niccokunzmann/freifunk-website-proxy
   ```
   Now, the server should be available at http://localhost.
3. Once the server is available, you need to configure the router of yours to forward the traffic.
   I.e. this could be your internet gateway available at http://192.168.0.1.
   Somewhere you can find the "Port Forwarding" (DE: Portfreigabe/Portweiterleitung)
   Here, you can configure the gateway to forward traffic from port 80 to your IP on port 80.
4. Setup a domain name.
   In case you have just a home router, you can use e.g. http://selfhost.eu to get a free of charge dynamic domain name.
5. In order for other people to reach not only your domain name but also other services on this domain,
   you need to setup a cname record.
   - Example:
     You registered `quelltext.selfhost.eu` free of charge.
     Now, you pay 2€/year and you buy `quelltext.eu`.
     Then, you setup the CNAME record `*.quelltext.eu` to point to `quelltext.selfhost.eu`.
   - You can also contact @niccokunzmann in an issue if you like to use a domain named `my-community.quelltext.eu`.
   - Your community has a website e.g. `freifunk-potsdam.de`.
     They can setup `service.freifunk-potsdam.de` and `*.service.freifunk-potsdam.de` to point to your domain.
6. Configure your gateway to update the IP address behind the domain name.
   Your gateway usually has a dyndns configuration which you can configure.
   This will update the registered dynamic domain name once your provider switches your IP address.

Once these steps are undergone, you should be able to access your server from the internet using your domain and
be able to register new clients.
Note that this looks like a lot bot this would be necessary for many more people to provide their services.
Once this is done, they have a much easier process to share their site.

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

    docker build --tag niccokunzmann/freifunk-website-proxy . && docker run -p "9000:80" -e "DOMAIN=localhost:9000" -it --rm niccokunzmann/freifunk-website-proxy

Now, you can reach your server under http://localhost:9000.

Run the tests

    watch -n 0.5 pytest

[ffp]: http://ffp.quelltext.eu
