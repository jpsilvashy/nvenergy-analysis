# Configuration file for JupyterHub

c = get_config()

# Use DummyAuthenticator for simple username/password auth
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
c.DummyAuthenticator.password = "jupyterhub"  # Use 'jupyterhub' as the password

# Set a single allowed user
c.Authenticator.allowed_users = {'jovyan'}
c.Authenticator.admin_users = {'jovyan'}

# Use the default spawner (simple notebook server per user)
c.JupyterHub.spawner_class = 'simple'

# Database configuration for PostgreSQL
c.JupyterHub.db_url = 'postgresql://jovyan:jupyterhub@db:5432/jupyterhub'

# Use JupyterLab by default
c.Spawner.default_url = '/lab'

# Explicitly set notebook directory
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

# Set the correct home directory
c.Spawner.home_dir = '/home/jovyan'

# Set the user's working directory
c.Spawner.notebook_dir = '/home/jovyan/work'

# Ensure JupyterLab opens in the correct directory
c.ServerApp.root_dir = '/home/jovyan'

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081
c.ConfigurableHTTPProxy.api_url = 'http://127.0.0.1:8001'

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = '/data/jupyterhub_cookie_secret'

c.JupyterHub.allow_named_servers = True
