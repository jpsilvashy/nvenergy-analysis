FROM jupyterhub/jupyterhub:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install JupyterHub, DockerSpawner, and other required packages
RUN pip3 install --no-cache-dir \
    dockerspawner \
    jupyter_client \
    sqlalchemy \
    psycopg2-binary \
    jupyterlab \
    pandas \
    matplotlib \
    seaborn \
    scipy

# Remove conflicting Node.js packages
RUN apt-get update && apt-get remove -y nodejs npm libnode-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install NodeJS 18.x and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs \
    && npm install -g configurable-http-proxy

# Create a jovyan user (matches the user in jupyter/datascience-notebook)
RUN useradd -m -s /bin/bash -N -u 1000 jovyan

# Create necessary directories and set permissions
RUN mkdir -p /data /home/jovyan/work /home/jovyan/data \
    && chown -R jovyan:users /data /home/jovyan

WORKDIR /home/jovyan

# Copy the Python script and data files
COPY --chown=jovyan:users nv_energy_analysis.py /home/jovyan/work/
COPY --chown=jovyan:users utils.py /home/jovyan/work/
COPY --chown=jovyan:users main.ipynb /home/jovyan/work/
COPY --chown=jovyan:users data/usage-data-*.zip /home/jovyan/work/data/

# Copy start script
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh && \
    chown jovyan:users /usr/local/bin/start.sh

USER jovyan

CMD ["/usr/local/bin/start.sh"]