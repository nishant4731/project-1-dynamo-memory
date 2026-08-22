FROM public.ecr.aws/docker/library/ubuntu:24.04@sha256:0d39fcc8335d6d74d5502f6df2d30119ff4790ebbb60b364818d5112d9e3e932

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip \
    && pip install --no-cache-dir --break-system-packages pytest==8.4.1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p /app/data
COPY data /app/data
COPY dragnet_io.py /app/dragnet_io.py
RUN chmod 0444 /app/dragnet_io.py

# A sealed pristine copy of the crashed dragnet, so a half-finished restitch of
# the live one is recoverable and the live run need not be held back to the end.
# An archive rather than a directory: it cannot be mistaken for a second dragnet
# to restitch, and unpacking it restores the shipped modes as well as the bytes.
RUN tar -C /app/data -cf /app/data/dragnet.spare.tar dragnet \
    && chmod 0444 /app/data/dragnet.spare.tar
