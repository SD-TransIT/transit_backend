# Superset specific config
import os

ROW_LIMIT = 5000

SUPERSET_WEBSERVER_PORT = 8088

# Secret key used by superset is same as django one
DEFAULT_SECRET_KEY = 'django-insecure-omy3k4lyrq7w8ij3uw&py!%hf@c4@4kub+mi9r-(dnn=(7=dl$'
SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres'),
DB_HOST = os.getenv('DB_HOST', '127.0.0.1'),
DB_PORT = os.getenv('DB_PORT', '5432'),
DB_NAME = os.getenv('DB_PORT', 'superset'),
SQLALCHEMY_DATABASE_URI = F'postgresql://{DB_USER}:{DB_PASSWORD}>@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''
