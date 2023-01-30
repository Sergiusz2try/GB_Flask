from flask import Blueprint, request, current_app, redirect, url_for
from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from werkzeug.exceptions import NotFound

from blog.config.extansions import db
from blog.forms.article import CreateArticleForm
from blog.models import Article, Author, Tag

articles = Blueprint(
    'articles',
    __name__,
    url_prefix='/articles',
    static_folder='../static',
    template_folder="../templates"
)


@articles.route('/', endpoint='list')
def articles_list():
    ARTICLES = Article.query.all()
    return render_template('articles/list.html', articles=ARTICLES)


@articles.route('/<int:pk>', endpoint='details')
def articles_detail(pk):
    article = Article.query.filter_by(id=pk).options(
        joinedload(Article.tags)
    ).one_or_none()
    if article is None:
        raise NotFound()
    return render_template('articles/details.html', article=article)


@articles.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    article = Article(title=form.title.data, body=form.body.data)

    # add tags to form
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)

        db.session.add(article)
        if current_user.author:
            # use existing author if present
            article.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author = current_user.author

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles.details", pk=article.id))

    return render_template("articles/create.html", form=form, error=error)
