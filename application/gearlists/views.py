from application import app, db
from application.gearlists.models import GearList
from application.gearlists.forms import ListsForm
from application.articles.models import Article
from flask_login import login_required, current_user

# flask
from flask import redirect, render_template, request, url_for
from flask_login import login_required

# Listing gearlists
@app.route("/lists", methods=["GET"])
def lists_index():
    usrLists = None
    
    if current_user.is_authenticated:
        usrLists = GearList.user_lists(current_user.id)#current_user.gearlists
        lists = GearList.not_user_lists(1)
    else:
        lists = GearList.not_user_lists(-1)

    return render_template("gearlists/list.html", 
                            lists = lists, usrLists = usrLists)

# New gearlist form
@app.route("/lists/new/")
@login_required
def lists_form():
    return render_template("gearlists/new.html", form = ListsForm())

# Adding new gearlist
@app.route("/lists", methods=["POST"])
@login_required
def list_create():
    form = ListsForm(request.form)

    t = GearList(form.name.data)
    t.description = form.description.data
    t.user = current_user.id

    db.session().add(t)
    db.session().commit()
    return redirect(url_for("gearlists_index"))

# Modify existing gearlist todo:delete gearlist
@app.route("/lists/<list_id>", methods=["GET", "POST"])
@login_required
def modify_list(list_id):
    gearlist = GearList.query.get(list_id)
    params = GearList.items_weight_volume(list_id)

    if request.method == "GET":
        return render_template("gearlists/modify.html", 
                                gearlist = gearlist, 
                                articles = current_user.items, 
                                useritems = gearlist.articles,
                                params = params)

# Adding items to a gearlist
@app.route("/lists/<list_id>/<item_id>", methods=["POST"])
@login_required
def additem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Article.query.get(item_id)

    gearlist.articles.append(item)
    db.session.commit()
    
    return render_template("gearlists/modify.html", 
                            gearlist = gearlist, 
                            articles = current_user.items,
                            useritems = gearlist.articles)

# Remove item from a gearlist
@app.route("/lists/rm/<list_id>/<item_id>", methods=["POST"])
@login_required
def rmItem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Article.query.get(item_id)

    gearlist.articles.remove(item)
    db.session.commit()

    return render_template("gearlists/modify.html", 
                            gearlist = gearlist, 
                            articles = current_user.items,
                            useritems = gearlist.articles)
