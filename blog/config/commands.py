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
            User(username=username, email=email, password=password, is_staff=True)
        )

        db.session.commit()


@click.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
        ]:
            tag = Tag(name=name)
            db.session.add(tag)

    db.session.commit()
    print("Created success!")
