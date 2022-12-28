from flask import Blueprint
from flask import render_template
from werkzeug.exceptions import NotFound


users = Blueprint('users', __name__, url_prefix='/users', static_folder='../static')

USERS = {
    1: "Alex",
    2: "Bob",
    3: "Carol",
}


@users.route('/', endpoint='list')
def users_list():
    return render_template('users/users.html', users=USERS)


@users.route('/<int:pk>', endpoint='details')
def details(pk):
    try:
        user = USERS[pk]
    except KeyError:
        raise NotFound(f'User #{pk} not found')
    return render_template('users/details.html', users=USERS, pk=pk)
