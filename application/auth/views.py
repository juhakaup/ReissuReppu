from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

# Login
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    # Login form
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())
    
    # Form validation
    form = LoginForm(request.form)
    if not form.validate():
        return render_template("auth/loginform.html", form = form)
    
    # Check if user in db
    user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, 
                error = "No such email or password")
    login_user(user)
    return redirect(url_for("lists_index"))

# Register new user
@app.route("/auth/register", methods = ["GET","POST"])
def register_user():
    # Registeration form
    if request.method == "GET":
        return render_template("auth/new.html", form = RegisterForm())
    
    # Form validation
    form = RegisterForm(request.form) 
    if not form.validate():
        return render_template("auth/new.html", form = form)

    # Adding new user to db
    user = User(form.email.data, form.password.data)
    user.name = form.name.data
    db.session().add(user)
    db.session().commit()
    return redirect(url_for("auth_login"))

# Logout user
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
