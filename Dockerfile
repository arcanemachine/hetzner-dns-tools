# syntax=docker/dockerfile:1

FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create a non-root user
ARG USERNAME=user
RUN useradd --create-home --shell /bin/bash --no-log-init $USERNAME


### INSTALL DEPENDENCIES ###

# git
RUN apt-get update && apt-get install git -y

# python build tools
RUN python3 -m pip install build


### SETUP ENVIRONMENT ###

# use non-root user
USER $USERNAME

# create and work in the directory that will contain the repo
ENV REPO_FOLDER=/home/user/hetzner-dns-tools
RUN mkdir -p $REPO_FOLDER
WORKDIR $REPO_FOLDER

# ensure ~/.local/bin exists in PATH
ARG LOCAL_BIN_FOLDER=/home/user/.local/bin
RUN mkdir -p $LOCAL_BIN_FOLDER
ENV PATH="${PATH}:$LOCAL_BIN_FOLDER"


### COMMANDS ###

# clone the repo
ENV REPO_URL="https://github.com/arcanemachine/hetzner-dns-tools"
ENV REPO_FOLDER="$REPO_FOLDER"
ENTRYPOINT git clone $REPO_URL $REPO_FOLDER\
    && python3 -m build\
    && python3 -m pip install .\
    && tail -f /dev/null
