from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.exceptions import NotFound

from blog.config.extansions import login_manager, db
from blog.forms.user import UserRegisterForm, LoginForm

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
    if current_user.is_authenticated:
        return redirect("users")

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template("auth/login.html", form=form, error="username doesn't exist")
        # if not user.password(form.password.data):
        #     return render_template("auth/login.html", form=form, error="invalid username or password")
        login_user(user)
        return redirect(url_for("users.list"))
    return render_template("auth/login.html", form=form)


@auth_app.route("/login-as/", methods=["GET", "POST"], endpoint="login-as")
def login_as():
    if not (current_user.is_authenticated and current_user.is_staff):
        # non-admin users should not know about this feature
        raise NotFound


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
            password=generate_password_hash(form.password.data),
            is_staff=False
        )

        db.session.add(_user)
        db.session.commit()

        login_user(_user)
        redirect(url_for("articles.list"))

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
