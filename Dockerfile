

FROM kurento
WORKDIR /tmp

RUN apt-get update -qq \
    && apt-get install -qq --yes --no-install-recommends \
        libkrb5-dev \
        libsodium23 \
	libzmq5-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /tmp
COPY c-n-vpipeline_0.0.1~rc1_amd64.deb pipe-connector.deb
RUN dpkg -i pipe-connector.deb

