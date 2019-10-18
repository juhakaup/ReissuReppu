from application import app, db
from application.items.models import Item
from application.items.forms import ItemForm
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

import copy

# Lists all the items
@app.route("/items", methods=["GET"])
def items_index():
    userItems = None
    otherItems = Item.non_user_items(-1) #Item.query.all()

    if current_user.is_authenticated:
        userItems = Item.user_items(current_user.id)
        otherItems = Item.non_user_items(current_user.id)
        
    return render_template("items/list.html", items = otherItems, userItems = userItems)

# Adding new item to db
@app.route("/items/new/", methods=["POST", "GET"])
@login_required
def item_create():
    # New item form
    if request.method=="GET":
        return render_template("items/new.html", form = ItemForm())

    # Form validation
    form = ItemForm(request.form)
    if not form.validate():
        return render_template("items/new.html", form = form)

    # Adding new item to db
    item = Item(form.name.data)
    item.brand = form.brand.data
    item.category = form.category.data
    item.weight = form.weight.data
    item.volume = form.volume.data
    item.description = form.description.data
    item.user_id = current_user.id

    db.session().add(item)
    db.session().commit()

    return redirect(url_for("items_index"))

# Adding a copy of an item to db for current user
@app.route("/items/copy/<item_id>", methods=["POST"])
@login_required
def item_copy(item_id):
    item = Item.query.get(item_id)
    newItem = Item(item.name)
    newItem.brand = item.brand
    newItem.category = item.category
    newItem.weight = item.weight
    newItem.volume = item.volume
    newItem.description = item.description
    newItem.user_id = current_user.id

    db.session().add(newItem)
    db.session().commit()

    return redirect(url_for("items_index"))

# Editing existing item form
@app.route("/items/edit/<item_id>", methods=["GET"])
@login_required
def item_edit(item_id):
    item = Item.query.get(item_id)
    
    form = ItemForm()
    form.name.data = item.name
    form.brand.data = item.brand
    form.category.data = item.category
    form.weight.data = item.weight
    form.volume.data = item.volume
    form.description.data = item.description
    form.user_id.data = item.user_id
    form.id.data = item_id
    
    return render_template("items/modify.html", form = form)

# Editing existing item
@app.route("/items/update/<item_id>", methods=["POST"])
@login_required
def item_update(item_id):
    item = Item.query.get(item_id)
    
    form = ItemForm(request.form)
    form.id.data = item_id
    # Form validation
    if not form.validate():
        return render_template("items/modify.html", form = form)

    # Update item in db
    item.name = form.name.data
    item.brand = form.brand.data
    item.category = form.category.data
    item.weight = form.weight.data
    item.volume = form.volume.data
    item.description = form.description.data
    
    db.session().commit()

    return redirect(url_for("items_index"))

# Delete item from db
@app.route("/items/rm/<item_id>", methods=["POST"])
@login_required
def item_rm(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()

    userItems = Item.user_items(current_user.id)
    otherItems = Item.non_user_items(current_user.id)

    return render_template("items/list.html", items = otherItems, userItems = userItems)