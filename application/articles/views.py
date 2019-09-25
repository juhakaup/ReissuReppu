from application import app, db
from application.articles.models import Article
from application.articles.forms import ArticleForm
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

# lists all the articles
@app.route("/articles", methods=["GET"])
def articles_index():
    return render_template("articles/list.html", articles = Article.query.all())

# form for adding new article
@app.route("/articles/new/")
def articles_form():
    return render_template("articles/new.html", form = ArticleForm(), title = "Add new item", commit = "Add", edit=False)

# adding new article to db
@app.route("/articles/", methods=["POST"])
@login_required
def article_create():
    form = ArticleForm(request.form)

    if not form.validate():
        return render_template("articles/new.html", form = form)

    item = Article(form.name.data)
    updateItem(item, form)
    
    db.session().add(item)
    db.session().commit()

    return redirect(url_for("articles_index"))

# editing existing article
@app.route("/articles/edit/<article_id>", methods=["GET", "POST"])
@login_required
def article_edit(article_id):
    item = Article.query.get(article_id)
    
    if request.method == "GET":
        form = ArticleForm()
        form.name.data = item.name
        form.brand.data = item.brand
        form.category.data = item.category
        form.weight.data = item.weight
        form.volume.data = item.volume
        form.description.data = item.description
        form.user.data = item.user
        form.id.data = article_id
        
        return render_template("articles/new.html", 
            form = form, title = "Update item", 
            commit = "Update", edit=True)
    
    uform = ArticleForm(request.form)    
    updateItem(item, uform)

    db.session().commit()

    return redirect(url_for("articles_index"))

# update article with data from form
def updateItem(article, form):
    article.name = form.name.data
    article.brand = form.brand.data
    article.category = form.category.data
    article.weight = form.weight.data
    article.volume = form.volume.data
    article.description = form.description.data
    article.user = current_user.id

# delete article from db
@app.route("/articles/rm/<article_id>", methods=["POST"])
@login_required
def article_rm(article_id):
    item = Article.query.get(article_id)
    db.session.delete(item)
    db.session.commit()

    return render_template("articles/list.html", articles = Article.query.all())