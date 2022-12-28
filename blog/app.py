from flask import Flask

from blog.users.views import users
from blog.articles.views import articles


def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(users)
    app.register_blueprint(articles)
