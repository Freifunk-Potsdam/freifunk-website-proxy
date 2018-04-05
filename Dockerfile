FROM alpine

# Install Python 3
RUN apk add --no-cache python3 && rm -rf /var/cache/apk/*

# make some useful symlinks that are expected to exist
RUN if [[ ! -e /usr/bin/python ]];        then ln -sf /usr/bin/python3 /usr/bin/python; fi
RUN if [[ ! -e /usr/bin/python-config ]]; then ln -sf /usr/bin/python3-config /usr/bin/python-config; fi
RUN if [[ ! -e /usr/bin/pydoc ]];         then ln -sf /usr/bin/pydoc3 /usr/bin/pydoc; fi
RUN if [[ ! -e /usr/bin/easy_install ]];  then ln -sf $(ls /usr/bin/easy_install*) /usr/bin/easy_install; fi
    
# Install and upgrade Pip
RUN easy_install pip && pip install --upgrade --no-cache-dir pip
RUN if [[ ! -e /usr/bin/pip ]]; then ln -sf /usr/bin/pip3 /usr/bin/pip; fi

# Install nginx
RUN apk add --update nginx && rm -rf /var/cache/apk/*
RUN chown -R nginx:www-data /var/lib/nginx

EXPOSE 80 443

# Create app environment
RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED=true

# Install Packages
ADD requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Start service
ENTRYPOINT ["/bin/sh", "start-service.sh"]
ADD start-service.sh .

# Add the app
ADD freifunk_website_proxy freifunk_website_proxy

