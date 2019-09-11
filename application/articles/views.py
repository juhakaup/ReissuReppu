from application import app, db
from flask import render_template, request
from application.articles.models import Article

@app.route("/articles/new/")
def articles_form():
    return render_template("articles/new.html")

@app.route("/articles/", methods=["POST"])
def article_create():
    t = Article(request.form.get("name"))

    db.session().add(t)
    db.session().commit()

    return "hello world!"