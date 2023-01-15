from flask import Blueprint
from flask import render_template

from werkzeug.exceptions import NotFound


articles = Blueprint(
    'articles',
    __name__,
    url_prefix='/articles',
    static_folder='../static',
    template_folder="../templates"
)

ARTICLES = {
    1: {
        "title": "lorem ipsum dolor sit 1",
        "text": "lorem ipsum dolor sit lorem sit lore mauris vel aug def def text",
        "author": 1
    },
    2: {
        "title": "lorem ipsum dolor sit 2",
        "text": "lorem ipsum dolor sit lorem sit lore mauris vel aug def def text",
        "author": 2
    },
    3: {
        "title": "lorem ipsum dolor sit 3",
        "text": "lorem ipsum dolor sit lorem sit lore mauris vel aug def def text",
        "author": 3
    }
}


@articles.route('/', endpoint='list')
def articles_list():
    return render_template('articles/articles.html', articles=ARTICLES)


@articles.route('/<int:pk>', endpoint='details')
def get_details(pk: int):
    try:
        article = ARTICLES[pk]
    except KeyError:
        raise NotFound(f'Page with id {pk} not found')
    return render_template('articles/details.html', pk=pk, articles=ARTICLES)
