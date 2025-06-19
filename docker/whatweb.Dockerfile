FROM ruby:3.0-alpine

# Install dependencies (no sudo needed in Dockerfiles)
RUN apk add --no-cache git make gcc musl-dev && \
    git clone https://github.com/urbanadventurer/WhatWeb.git /whatweb && \
    cd /whatweb && \
    gem install bundler && \
    bundle install && \
    apk del make gcc musl-dev  # Remove build tools after installation

WORKDIR /whatweb
ENV PATH="/whatweb:${PATH}"

ENTRYPOINT ["ruby", "whatweb"]