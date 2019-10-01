from application import app, db
from application.gearlists.models import GearList
from application.gearlists.forms import ListsForm
from application.items.models import Item
from flask_login import login_required, current_user

# flask
from flask import redirect, render_template, request, url_for
from flask_login import login_required

# Listing gearlists
@app.route("/lists", methods=["GET"])
def lists_index():
    userLists = None
    
    if current_user.is_authenticated:
        userLists = GearList.user_lists(current_user.id)#current_user.gearlists
        allLists = GearList.not_user_lists(1)
    else:
        allLists = GearList.not_user_lists(-1)

    return render_template("gearlists/list.html", 
                            allLists = allLists, userLists = userLists)

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
    return redirect(url_for("lists_index"))

# Modify existing gearlist todo:delete gearlist
@app.route("/lists/<list_id>", methods=["GET", "POST"])
@login_required
def modify_list(list_id):
    gearlist = GearList.query.get(list_id)
    params = GearList.items_weight_volume(list_id)

    if request.method == "GET":
        return render_template("gearlists/modify.html", 
                                gearlist = gearlist, 
                                items = current_user.items, 
                                useritems = gearlist.items,
                                params = params)

# Adding items to a gearlist
@app.route("/lists/<list_id>/<item_id>", methods=["POST"])
@login_required
def additem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Item.query.get(item_id)

    gearlist.items.append(item)
    db.session.commit()
    
    return render_template("gearlists/modify.html", 
                            gearlist = gearlist, 
                            items = current_user.items,
                            useritems = gearlist.items)

# Remove item from a gearlist
@app.route("/lists/rm/<list_id>/<item_id>", methods=["POST"])
@login_required
def rmItem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Items.query.get(item_id)

    gearlist.items.remove(item)
    db.session.commit()

    return render_template("gearlists/modify.html", 
                            gearlist = gearlist, 
                            items = current_user.items,
                            useritems = gearlist.items)
