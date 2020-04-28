from flask import Flask

def create_app(config_filename=None):
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)

    with app.app_context():
        # http routes 
        from . import routes
        return app