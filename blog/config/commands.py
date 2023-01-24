import click
from werkzeug.security import generate_password_hash

from blog.config.extansions import db


@click.command("create-admin")
def create_admin():
    """Create a admin."""
    from blog.models import User
    from wsgi import app

    username = input("Username: ")
    email = input("Email: ")
    password = generate_password_hash(input("Password: "))

    with app.app_context():
        db.session.add(
            User(username=username, email=email, password=password)
        )

        db.session.commit()
