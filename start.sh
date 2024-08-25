#!/bin/bash

# Wait for the database to be ready
until pg_isready -h db -U jovyan -d jupyterhub; do
  echo "Waiting for database to be ready..."
  sleep 2
done

# Upgrade the database schema
jupyterhub upgrade-db

# Start JupyterHub
exec jupyterhub -f /srv/jupyterhub/jupyterhub_config.py