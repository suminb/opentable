import os
import sys

from flask import Flask
from flask_cors import CORS
from logbook import Logger, StreamHandler


__version__ = '0.1.0'


StreamHandler(sys.stderr).push_application()
log = Logger('koob')

DEFAULT_DB_URL = 'sqlite:///dev.db'


def create_app(name=__name__, config={}):
    app = Flask(name)
    app.secret_key = os.environ.get('SECRET', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        os.environ.get('DB_URL', DEFAULT_DB_URL)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = bool(os.environ.get('KOOB_DEBUG', False))
    app.config.update(config)

    CORS(app, resources={r'/api/v1/*': {'origins': '*'}})

    from koob.models import db, KoobJSONEncoder
    db.init_app(app)
    app.json_encoder = KoobJSONEncoder

    from koob.api import api_module
    app.register_blueprint(api_module, url_prefix='/api')

    return app


if __name__ == '__main__':
    host = os.environ.get('KOOB_HOST', '0.0.0.0')
    port = int(os.environ.get('KOOB_PORT', 8080))
    app = create_app()
    app.run(host=host, port=port)