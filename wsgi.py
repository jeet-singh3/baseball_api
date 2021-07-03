from app.routes import create_app
from app.config.config import get_config_by_env

app = create_app(get_config_by_env())

if __name__ == 'main':
    app.run(host='0.0.0.0', port=5000)
