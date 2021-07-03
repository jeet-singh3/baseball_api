import os

from app.routes import create_app
from app.config.config import get_config_by_env
from app.utils.migrate import initial_table_creation


os.environ["PG_USER"] = "postgres"
os.environ["PG_PASS"] = "postgres"
os.environ["PG_HOST"] = "postgres"
os.environ["PG_HOST_READ"] = "postgres"
os.environ["PG_PORT"] = "5432"
os.environ["PG_NAME"] = "postgres"

app = create_app(get_config_by_env('testing'))
initial_table_creation()
