from blog.app import create_app
from blog.models import User
from blog.models.database import db

app = create_app()


@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Done!")


@app.cli.command("create-user")
def create_user():
    """Create a new user."""
    username = input("Username: ")
    email = input("Email: ")

    user = User(username=username, email=email)

    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
    )
