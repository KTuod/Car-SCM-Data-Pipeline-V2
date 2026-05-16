FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && rm -f /etc/apt/sources.list.d/yarn.list.save

RUN curl -LsSf https://getbruin.com/install/cli | sh \
    && mv ~/.local/bin/bruin /usr/local/bin/bruin \
    && chmod +x /usr/local/bin/bruin

RUN apt-get update && apt-get install -y unzip \
    && curl -O -L "https://github.com/grafana/loki/releases/download/v2.9.4/promtail-linux-amd64.zip" \
    && unzip promtail-linux-amd64.zip \
    && mv promtail-linux-amd64 /usr/local/bin/promtail \
    && chmod a+x /usr/local/bin/promtail \
    && rm promtail-linux-amd64.zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*