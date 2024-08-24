# Configuration file for JupyterHub

c = get_config()

# Use PAM for local user authentication
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

# Create a test user (in a real scenario, you'd manage users differently)
c.Authenticator.admin_users = {'jovyan'}

# Use the DockerSpawner to spawn user notebooks
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Spawn containers from this image
c.DockerSpawner.image = 'jupyter/datascience-notebook:latest'

# Connect containers to this Docker network
c.DockerSpawner.network_name = 'jupyterhub'

# Explicitly set notebook directory
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = '/data/jupyterhub_cookie_secret'
c.JupyterHub.db_url = 'sqlite:////data/jupyterhub.sqlite'

# Use JupyterLab by default
c.Spawner.default_url = '/lab'

# Allow multiple users to login
c.JupyterHub.allow_named_servers = True