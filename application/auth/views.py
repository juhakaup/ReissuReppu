from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, login_required, bcrypt
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
    
    # Check if user in db and password match
    user = User.query.filter_by(email=form.email.data).first()
    if not user or not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form = form, 
                error = "No such email or password")
    
    login_user(user)
    return redirect(url_for("lists_index"))

# Register new user
@app.route("/auth/register", methods = ["GET","POST"])
def register_user():
    # Registeration form
    if request.method == "GET":
        return render_template("auth/new.html", form = RegisterForm(), error="")
    
    # Form validation
    form = RegisterForm(request.form) 
    if not form.validate():
        return render_template("auth/new.html", form = form, error="")

    user = User(form.email.data, form.password.data)
    user.name = form.name.data

    # Check for existing user with the same email
    if User.query.filter_by(email=user.email).first():
        return render_template("auth/new.html", form = form, error="An account with this email already exists")
    
    # Adding new user to db
    db.session().add(user)
    db.session().commit()
    return redirect(url_for("auth_login"))

# Logout user
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

# Userlist
@app.route("/auth/")
@login_required(role="ADMIN")
def list_users():
    users = User.query.all()
    for user in users:
        print(user.name)

    return redirect(url_for("lists_index"))


