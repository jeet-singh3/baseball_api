from app.routes import create_app
from app.config.config import get_config_by_env
from app.utils.migrate import initial_table_creation


app = create_app(get_config_by_env('testing'))
initial_table_creation()
