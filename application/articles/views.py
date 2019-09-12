from application import app, db
from flask import redirect, render_template, request, url_for
from application.articles.models import Article

@app.route("/articles", methods=["GET"])
def articles_index():
    return render_template("articles/list.html", articles = Article.query.all())

@app.route("/articles/new/")
def articles_form():
    return render_template("articles/new.html")

@app.route("/articles/", methods=["POST"])
def article_create():
    t = Article(request.form.get("name"),
    request.form.get("brand"),
    request.form.get("weight"),
    request.form.get("volume"),
    request.form.get("description"))

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("articles_index"))