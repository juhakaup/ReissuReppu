from application import app, db
from application.gearlists.models import GearList
from application.gearlists.forms import ListsForm
from application.items.models import Item
from flask_login import login_required, current_user

# flask
from flask import redirect, render_template, request, url_for
from flask_login import login_required

# Listing all gearlists
@app.route("/lists", methods=["GET"])
def lists_index():  
    userLists = None
    if current_user.is_authenticated:
        userLists = GearList.user_lists(current_user.id)
    return render_template("gearlists/list.html", allLists = GearList.all_lists(), userLists = userLists)

# Viewing a gearlist
@app.route("/lists/<list_id>", methods=["GET"])
def view_list(list_id):
    gearlist = GearList.query.get(list_id)
    return render_template("gearlists/view.html", gearlist = gearlist, items = gearlist.items, )

# Creating new gearlist
@app.route("/lists/new/", methods=["POST", "GET"])
@login_required
def list_create():
    # form for creating new gearlist
    if request.method=="GET":
        return render_template("gearlists/new.html", form = ListsForm())

    # adding new gearlist to db
    form = ListsForm(request.form)
    gearlist = GearList(name=form.name.data, user_id=current_user.id, description=form.description.data)
    db.session().add(gearlist)
    db.session().commit()

    return render_template("gearlists/modify.html", gearlist = gearlist, items = gearlist.items, 
                            availableItems = gearlist.available_items(current_user.id), form = form)

# Modify existing gearlist form
@app.route("/lists/modify/<list_id>", methods=["POST"])
@login_required
def modify_list(list_id):
    gearlist = GearList.query.get(list_id)
    
    if not (gearlist.user_id == current_user.id or current_user.has_role("ADMIN")):
        return redirect(url_for("lists_index"))
    
    form = ListsForm()
    form.name.data = gearlist.name
    form.description.data = gearlist.description

    return render_template("gearlists/modify.html", gearlist = gearlist, items = gearlist.items, 
                            availableItems = gearlist.available_items(current_user.id), form = form)

# Update existing gearlist
@app.route("/lists/<list_id>", methods=["POST"])
@login_required
def update_list(list_id):
    gearlist = GearList.query.get(list_id)
    
    if not (gearlist.user_id == current_user.id or current_user.has_role("ADMIN")):
        return redirect(url_for("lists_index"))

    form = ListsForm(request.form)
    gearlist.name = form.name.data
    gearlist.description = form.description.data
    db.session.commit()
    
    availableItems = gearlist.available_items(current_user.id)
    return render_template("gearlists/modify.html", gearlist = gearlist, items = gearlist.items, 
                            availableItems = availableItems, form = form)

# Remove gearlist
@app.route("/lists/rm/<list_id>", methods=["POST"])
@login_required 
def delete_list(list_id):   
    gearlist = GearList.query.get(list_id)
    if not (gearlist.user_id == current_user.id or current_user.has_role("ADMIN")):
        return redirect(url_for("lists_index"))
    for item in gearlist.items:
        gearlist.items.remove(item)
        db.session.commit()
    db.session.delete(gearlist)
    db.session.commit()
    
    return redirect(url_for("lists_index"))


# Adding items to a gearlist
@app.route("/lists/<list_id>/<item_id>", methods=["POST"])
@login_required
def additem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Item.query.get(item_id)

    gearlist.items.append(item)
    db.session.commit()

    form = ListsForm()
    form.name.data = gearlist.name
    form.description.data = gearlist.description

    availableItems = gearlist.available_items(current_user.id)
    return render_template("gearlists/modify.html", 
                            gearlist = gearlist, items = gearlist.items, 
                            availableItems = availableItems, form=form)

# Remove item from a gearlist
@app.route("/lists/rm/<list_id>/<item_id>", methods=["POST"])
@login_required
def rmItem_list(list_id, item_id):
    gearlist = GearList.query.get(list_id)
    item = Item.query.get(item_id)

    gearlist.items.remove(item)
    db.session.commit()

    form = ListsForm()
    form.name.data = gearlist.name
    form.description.data = gearlist.description

    availableItems = gearlist.available_items(current_user.id)
    return render_template("gearlists/modify.html", gearlist = gearlist, 
                            items = gearlist.items, 
                            availableItems = availableItems, form=form)
