from main import app_factory
from config import project_name
import os
from extensions import login_manager

try:
    config_obj_path = os.environ['FLASK_CONFIG_DEFAULT']
except KeyError:
    print(
        "Please, provide the environment variable FLASK_CONFIG_DEFAULT. "
        "It tells the application which configuration class to load.")
    exit()

app = app_factory(config_obj_path, project_name)
login_manager.init_app(app)
login_manager.login_view = 'login'

if __name__ == '__main__':
    _debug = app.config.get('DEBUG', False)

    kwargs = {
        'host': os.getenv('FLASK_HOST', '127.0.0.1'),
        'port': int(os.getenv('FLASK_PORT', 5000)),
        'debug': _debug,
        'use_reloader': app.config.get('USE_RELOADER', _debug),
        **app.config.get('SERVER_OPTIONS', {})
    }

    from extensions import io

    io.run(app, **kwargs)
    
# Trigger for xprocess testing server
print('Server ready')