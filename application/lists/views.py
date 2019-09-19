from application import app, db
from application.lists.models import GearList
from application.lists.forms import ListsForm
from flask_login import login_required, current_user

#flask
from flask import redirect, render_template, request, url_for
from flask_login import login_required

#listing gearlists
@app.route("/lists", methods=["GET"])
def lists_index():
    return render_template("lists/list.html", lists = GearList.query.all())

#adding new gearlist
@app.route("/lists", methods=["POST"])
def list_create():
    form = ListsForm(request.form)

    t = GearList(form.name.data)
    t.description = form.description.data
    t.user = current_user.id

    db.session().add(t)
    db.session().commit()
    return redirect(url_for("lists_index"))

#new gearlist form
@app.route("/lists/new/")
def lists_form():
    return render_template("lists/new.html", form = ListsForm())

