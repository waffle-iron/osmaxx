FROM golang:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      libprotobuf-dev \
      libleveldb-dev \
      libgeos-dev \
      postgresql-client \
      osmctools \
      --no-install-recommends \
 && ln -s /usr/lib/libgeos_c.so /usr/lib/libgeos.so \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/imposm3/go
ENV GOPATH=/home/imposm3/go

RUN go get github.com/tools/godep \
 && go get github.com/omniscale/imposm3 \
 && go install github.com/omniscale/imposm3

# Purge no longer needed packages to keep image small.
# Protobuf and LevelDB dependencies cannot be removed
# because they are dynamically linked.
RUN apt-get purge -y --auto-remove \
    g++ gcc libc6-dev make git \
    && rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:$GOPATH/bin/

ADD ./entrypoint.sh /entrypoint.sh

WORKDIR /home/example
ADD ./*.json /home/example/
ADD ./*.yml /home/example/

#ENTRYPOINT /entrypoint.sh
