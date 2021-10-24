FROM debian:buster-slim

RUN apt-get update && apt-get --no-install-recommends -y install zip unzip build-essential libtool autoconf automake pkg-config wget git sudo redis-server libjson-c-dev libssl-dev libcurl4-gnutls-dev libmaxminddb-dev libsqlite3-dev libreadline-dev libxml2-dev librrd-dev libpcap-dev libzmq3-dev debhelper fakeroot default-libmysqld-dev dpkg-sig libexpat1-dev net-tools && rm -rf /var/lib/apt/lists/*

# build nDPI
WORKDIR /usr/local/share/
RUN wget https://github.com/ntop/nDPI/archive/refs/tags/3.4.zip --no-check-certificate -O nDPI-3.4.zip
RUN unzip nDPI-3.4.zip && mv nDPI-3.4 nDPI
WORKDIR /usr/local/share/nDPI/
RUN ./autogen.sh; make -j4

# build ntopng
WORKDIR /usr/local/share/
RUN wget https://github.com/ntop/ntopng/archive/refs/tags/4.2.zip --no-check-certificate -O ntopng-4.2.zip
RUN unzip ntopng-4.2.zip && mv ntopng-4.2 ntopng
WORKDIR /usr/local/share/ntopng/
RUN ./autogen.sh && ./configure && make -j4

# put flag
COPY ./flag /flag
RUN chmod 0444 /flag

# put read flag script
COPY get_flagz.lua /usr/local/share/ntopng/scripts/lua/datasources/get_flagz.lua

COPY run.sh /usr/local/share/run.sh
WORKDIR /usr/local/share/
RUN chmod +x run.sh

CMD ["bash", "-c", "./run.sh"]