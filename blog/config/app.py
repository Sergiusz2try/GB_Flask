from flask import Flask

from blog.config import commands
from blog.models import User
from blog.config.extansions import db, login_manager, migrate

from blog.users.views import users
from blog.articles.views import articles
from blog.auth.views import auth_app


def create_app() -> Flask:
    app = Flask(__name__)

    CONFIG_NAME = "DevConfig"
    app.config.from_object(f"blog.config.config.{CONFIG_NAME}")

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    login_manager.login_view = "auth_app.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get_or_404(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(users)
    app.register_blueprint(articles)
    app.register_blueprint(auth_app)


def register_commands(app: Flask):
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_user)
