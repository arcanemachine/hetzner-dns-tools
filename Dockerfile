# syntax=docker/dockerfile:1

FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create a non-root user
ARG USERNAME=user
RUN useradd --create-home --shell /bin/bash --no-log-init $USERNAME

# install git
RUN apt-get update && apt-get install git -y

# install python build tools
RUN python3 -m pip install build

# use non-root user
USER $USERNAME

# ensure ~/.local/bin exists in PATH
RUN mkdir -p /home/user/.local/bin
ENV PATH="${PATH}:/home/user/.local/bin"

ARG REPO_FOLDER=/home/user/hetzner-dns-tools

# clone the repo
RUN git clone https://github.com/arcanemachine/hetzner-dns-tools $REPO_FOLDER

# work in the directory that contains the repo
WORKDIR $REPO_FOLDER

# build and install hetzner-dns-tools
RUN python3 -m build
RUN python3 -m pip install .
