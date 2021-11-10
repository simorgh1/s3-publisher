# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.194.3/containers/javascript-node/.devcontainer/base.Dockerfile

ARG VARIANT="16-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:0-${VARIANT}

LABEL authors="Bahram Maravandi"

#### Install required tools

RUN apt-get update -y && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends \
    python3 \
    zip \
    make \
    xdg-utils \
    python3-pip && \
    pip3 install shyaml cfn-lint aws-sam-cli

### Install awscliv2 for arm, for x86 read: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip
