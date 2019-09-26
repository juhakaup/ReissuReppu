from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, 
                error = "No such email or password")
    
    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET","POST"])
def register_user():
    if request.method == "GET":
        return render_template("auth/new.html", form = RegisterForm())
    
    form = RegisterForm(request.form)
    
    user = User(form.email.data, form.password.data)
    user.name = form.name.data
    
    if not form.validate():
        return render_template("auth/new.html", form = form, 
                error = "Please fill all the fiels")

    db.session().add(user)
    db.session().commit()
    return redirect(url_for("auth_login"))

