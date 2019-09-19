from application import app, db
from application.articles.models import Article
from application.articles.forms import ArticleForm
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

#lists all the articles
@app.route("/articles", methods=["GET"])
def articles_index():
    return render_template("articles/list.html", articles = Article.query.all())

#form for adding new article
@app.route("/articles/new/")
def articles_form():
    return render_template("articles/new.html", form = ArticleForm())

#adding new article to db
@app.route("/articles/", methods=["POST"])
@login_required
def article_create():
    form = ArticleForm(request.form)

    if not form.validate():
        return render_template("articles/new.html", form = form)

    t = Article(form.name.data)
    t.brand = form.brand.data
    t.category = form.category.data
    t.weight = form.weight.data
    t.volume = form.volume.data
    t.description = form.description.data
    t.user = current_user.id
    
    db.session().add(t)
    db.session().commit()

    return redirect(url_for("articles_index"))