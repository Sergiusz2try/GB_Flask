import click

from blog.config.extansions import db
from blog.models import User


@click.command("init-db")
def init_db():
    """Initialize the database."""
    from wsgi import app
    from blog.models import User

    db.create_all(app=app)
    print("Done!")


@click.command("create-user")
def create_user():
    """Create a new user."""
    from blog.models import User
    from wsgi import app

    username = input("Username: ")
    email = input("Email: ")

    with app.app_context():
        db.session.add(
            User(username=username, email=email)
        )

        db.session.commit()
