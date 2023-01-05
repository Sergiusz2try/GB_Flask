from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_user, login_required, logout_user
from blog.config.extansions import login_manager

from blog.models import User

auth_app = Blueprint("auth_app", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(pk):
    return User.query.filter_by(id=pk).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))


@auth_app.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    username = request.form.get("username")
    if not username:
        return render_template("auth/login.html", error="Username not passed")

    user = User.query.filter_by(username=username).one_or_none()
    if user is None:
        return render_template("auth/login.html", error="User not found")

    login_user(user, remember=True)
    return redirect(url_for("users.list"))


@auth_app.route("/logout", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_app.login"))


@auth_app.route("/secret")
@login_required
def secret_view():
    return "Super secret data!"


__all__ = [
    "login_manager",
    "auth_app",
]