import os
from flask import Flask
from dotenv import load_dotenv
from config.config import config
from utils.extensions import db

from api.comments import blueprint_comments
from api.posts import blueprint_posts
from api.users import blueprint_users

load_dotenv()
ENV = os.getenv('ENV', 'default')

if ENV not in config:
    raise Exception('Invalid ENV: %s' % ENV)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config[ENV]())
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register extensions."""
    db.init_app(app)
    return None


def register_blueprints(app):
    """Register blueprints."""
    app.register_blueprint(blueprint_posts)
    app.register_blueprint(blueprint_users)
    app.register_blueprint(blueprint_comments)

    return None
