FROM debian:trixie-slim@sha256:62bd423aeee912639ca8ee681c2b762cb3e25137e0a92b20be455898a9f034ad AS base

# Configuration
ENV DEBIAN_FRONTEND=noninteractive
USER root

# Install dependencies
RUN apt update && apt upgrade -y \
    && apt install --no-install-recommends -y \
        ca-certificates \
        bash \
        make \
        curl \
    && apt clean \
    && apt autoremove \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 user \
    && useradd \
        --uid 1000 \
        --gid user \
        --create-home \
        --home-dir /home/user \
        --shell /bin/bash \
        --skel /etc/skel \
        user \
    && passwd -d user \
    && chown -R user:user /home/user

# Switch to non-root user
USER user
WORKDIR /home/user

COPY --from=ghcr.io/astral-sh/uv:0.13.1@sha256:4a1f3666816dafadd20ceb71eac9a7d56d7ef30279f7d64048519ab901ada336 /uv /uvx /usr/local/bin/
ENV UV_LINK_MODE=copy

# Reset frontend to interactive
ENV DEBIAN_FRONTEND=dialog

