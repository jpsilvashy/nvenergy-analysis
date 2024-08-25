#!/bin/bash

# Set password for jovyan if JOVYAN_PASSWORD is set
if [ ! -z "$JOVYAN_PASSWORD" ]; then
    echo "jovyan:$(mkpasswd -m sha-512 $JOVYAN_PASSWORD)" | sudo chpasswd -e
fi

# Start JupyterHub
exec jupyterhub -f /srv/jupyterhub/jupyterhub_config.py