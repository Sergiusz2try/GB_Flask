from flask import Blueprint
from flask import render_template
from flask_login import login_required

from blog.models import User

users = Blueprint(
    'users',
    __name__,
    url_prefix='/users',
    static_folder='../static',
    template_folder="../templates"
)


@users.route('/', endpoint='list')
def users_list():
    USERS = User.query.all()
    return render_template('users/users.html', users=USERS)


@users.route('/<int:pk>', endpoint='details')
@login_required
def details(pk):
    user = User.query.get_or_404(pk)
    return render_template('users/details.html', user=user)
