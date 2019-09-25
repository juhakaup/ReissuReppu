from application import app, db
from application.lists.models import GearList
from application.lists.forms import ListsForm
from application.articles.models import Article
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
@login_required
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
@login_required
def lists_form():
    return render_template("lists/new.html", form = ListsForm())

# modify excisting gearlist
@app.route("/lists/<list_id>", methods=["GET", "POST"])
@login_required
def modify_list(list_id):
    gearlist = GearList.query.get(list_id)

    if request.method == "GET":
        return render_template("lists/modify.html", 
                                gearlist = gearlist, 
                                articles = Article.query.all(),
                                useritems = gearlist.articles)

# adding items to a gearlist
@app.route("/lists/<list_id>/<item_id>", methods=["POST"])
@login_required
def additem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Article.query.get(item_id)

    gearlist.articles.append(item)
    db.session.commit()
    
    return render_template("lists/modify.html", 
                                gearlist = gearlist, 
                                articles = Article.query.all(),
                                useritems = gearlist.articles)

# remove item from gearlist
@app.route("/lists/rm/<list_id>/<item_id>", methods=["POST"])
@login_required
def rmItem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Article.query.get(item_id)

    gearlist.articles.remove(item)
    db.session.commit()

    return render_template("lists/modify.html", 
                                gearlist = gearlist, 
                                articles = Article.query.all(),
                                useritems = gearlist.articles)
