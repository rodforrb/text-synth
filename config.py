import os
import logging

from datetime import timedelta
from typing import Dict
from typing import List

project_name = "text-synth"
SQLALCHEMY_DATABASE_URI_TMPL = "sqlite:////tmp/%(name)s.sqlite"


# base config class; extend it to your needs.
class Config(object):
    # see http://flask.pocoo.org/docs/1.0/config/#environment-and-debug-features
    ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'

    # use TESTING mode?
    TESTING = False

    # use server x-sendfile?
    USE_X_SENDFILE = False

    # should be the hostname of your project
    HOST = os.getenv('HOST', '')  # create an alias in /etc/hosts for dev
    # useful for development/testing mode
    # necessary if non-standard port is being used
    HOST_PORT = os.getenv('HOST_PORT', '')
    # we need to append the host port to the server_name if it is non-standard
    SERVER_NAME_EXTRA = len(HOST_PORT) and '' or (":" + HOST_PORT)
    # SERVER_NAME contains the hostname and port (if non-default)
    SERVER_NAME = HOST + SERVER_NAME_EXTRA


    DB_USER = os.getenv('DB_USER', '')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_HOST = os.getenv('DB_HOST', '')  # plus port, if non-default
    DB_NAME = os.getenv('DB_NAME', '')

    # default database connection
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_TMPL % {
        'user': DB_USER,
        'passwd': DB_PASS,
        'host': DB_HOST,
        'name': DB_NAME
    }

    # set this up case you need multiple database connections
    SQLALCHEMY_BINDS: Dict = {}

    # log all the statements issued to stderr?
    SQLALCHEMY_ECHO = DEBUG
    # track and emit signals on object modification?
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # use to set werkzeug / socketio options, if needed
    # SERVER_OPTIONS = {}
    WTF_CSRF_ENABLED = True
    # import os; os.urandom(24)
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "secret")

    # LOGGING
    LOGGER_NAME = "%s_log" % project_name
    LOG_FILENAME = "/var/tmp/app.%s.log" % project_name
    LOG_LEVEL = logging.INFO
    # used by logging.Formatter
    LOG_FORMAT = "%(asctime)s %(levelname)s\t: %(message)s"

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # EMAIL CONFIGURATION
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = os.getenv("FLASK_MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("FLASK_MAIL_PORT", "25"))
    MAIL_USE_TLS = os.getenv("FLASK_MAIL_USE_TLS", "") == "1"
    MAIL_USE_SSL = os.getenv("FLASK_MAIL_USE_SSL", "") == "1"
    MAIL_USERNAME = os.getenv("FLASK_MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("FLASK_MAIL_PASSWORD", None)
    DEFAULT_MAIL_SENDER = os.getenv(
        "FLASK_DEFAULT_MAIL_SENDER",
        "example@%s.com" % project_name
    )

    # these are the modules preemptively
    # loaded for each app
    LOAD_MODULES_EXTENSIONS = [
        'views',
        # 'models',
        # 'admin',
        # 'api',
        # 'schemas'
    ]

    # # add below the module path of extensions
    # # you wish to load
    EXTENSIONS = [
        'extensions.db',
        'extensions.migrate',
    #     'extensions.security',
    #     'extensions.ma',
    #     'extensions.glue',
        'extensions.io'
    ]

    BLUEPRINTS: List = [('text-synth', {'url_prefix': ''})]


# config class for development environment
class Dev(Config):
    MAIL_DEBUG = True
    # EXTENSIONS = Config.EXTENSIONS + [
    #     'extensions.toolbar'
    # ]
        # uses sqlite by default
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/%s.db' % Config.DB_NAME



# config class used during tests
class Test(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
