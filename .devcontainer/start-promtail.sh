#!/bin/bash

set -a
source /workspaces/scm-data-pipeline-v2/.env
set +a

nohup promtail -config.file=/workspaces/scm-data-pipeline-v2/.devcontainer/promtail-config.yml -config.expand-env=true > /tmp/promtail.out 2>&1 &

echo "Promtail started successfully with .env!"