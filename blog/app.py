from flask import Flask
from blog.models.database import db

from blog.users.views import users
from blog.articles.views import articles
from blog.views.auth import auth_app, login_manager


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "KpmuRUyKhU5NNlqfl2zGpKXDIG8hjHfu"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    login_manager.init_app(app)

    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(users)
    app.register_blueprint(articles)
    app.register_blueprint(auth_app)
