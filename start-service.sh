
mkdir -p /run/nginx

nginx -v
sleep 0.01

python3 -m freifunk_website_proxy

