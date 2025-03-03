
FROM ubuntu:20.04


ENV DEBIAN_FRONTEND=non-interactive


RUN apt-get update && apt-get install -y \
    build-essential \
    libtool \
    autotools-dev \
    automake \
    pkg-config \
    libssl-dev \
    libevent-dev \
    libboost-system-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-thread-dev \
    libboost-chrono-dev \
    libboost-test-dev \
    git \
    libdb-dev \ 
    && rm -rf /var/lib/apt/lists/*


RUN git clone --branch v22.0 https://github.com/bitcoin/bitcoin.git /bitcoin   


WORKDIR /bitcoin


RUN ./autogen.sh && \
    ./configure && \
    make


EXPOSE 8332


ENTRYPOINT ["./src/bitcoind"]