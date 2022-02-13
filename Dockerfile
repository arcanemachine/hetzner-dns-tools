# syntax=docker/dockerfile:1

FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create a non-root user
ARG USERNAME=user
RUN useradd --create-home --shell /bin/bash --no-log-init $USERNAME

# use non-root user
USER $USERNAME
WORKDIR /home/user

# install hetzner-dns-tools
RUN python3 -m pip install hetzner-dns-tools

# add hetzner-dns-tools folder to PATH
ENV PATH="${PATH}:/home/user/.local/bin"
