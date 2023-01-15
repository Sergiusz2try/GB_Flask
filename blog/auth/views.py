from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_user, login_required, logout_user, current_user
from blog.config.extansions import login_manager, db
from blog.forms.user import UserRegisterForm

from werkzeug.security import generate_password_hash

from blog.models import User

auth_app = Blueprint(
    "auth_app",
    __name__,
    static_folder="../static",
    template_folder="../templates"
)


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


@auth_app.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.details", pk=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []

    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("This email is already registered!")
            render_template("auth/register.html", form=form)

        _user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(_user)
        db.session.commit()

        login_user(_user)

    return render_template(
        "auth/register.html",
        form=form,
        errors=errors,
    )


@auth_app.route("/secret")
@login_required
def secret_view():
    return "Super secret data!"


__all__ = [
    "login_manager",
    "auth_app",
]