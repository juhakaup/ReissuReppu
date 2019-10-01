from application import app, db
from application.items.models import Item
from application.items.forms import ItemForm
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

# Lists all the items
@app.route("/items", methods=["GET"])
def items_index():
    userItems = None
    if current_user.is_authenticated:
        userItems = current_user.items
        
    return render_template("items/list.html", items = Item.query.all(), 
                            usrItems = userItems)

# Form for adding new item
@app.route("/items/new/")
def items_form():
    return render_template("items/new.html", form = ItemForm(), title = "Add new item", commit = "Add", edit=False)

# Adding new item to db
@app.route("/items/", methods=["POST"])
@login_required
def item_create():
    form = ItemForm(request.form)

    if not form.validate():
        return render_template("items/new.html", form = form)

    item = Item(form.name.data)
    updateItem(item, form)
    
    db.session().add(item)
    db.session().commit()

    return redirect(url_for("items_index"))

# Editing existing item
@app.route("/items/edit/<item_id>", methods=["GET", "POST"])
@login_required
def item_edit(item_id):
    item = Item.query.get(item_id)
    
    if request.method == "GET":
        form = ItemForm()
        form.name.data = item.name
        form.brand.data = item.brand
        form.category.data = item.category
        form.weight.data = item.weight
        form.volume.data = item.volume
        form.description.data = item.description
        form.user.data = item.user
        form.id.data = item_id
        
        return render_template("items/new.html", 
            form = form, title = "Update item", 
            commit = "Update", edit=True)
    
    uform = ItemForm(request.form)    
    updateItem(item, uform)

    db.session().commit()

    return redirect(url_for("items_index"))

# Update item with data from form
def updateItem(item, form):
    item.name = form.name.data
    item.brand = form.brand.data
    item.category = form.category.data
    item.weight = form.weight.data
    item.volume = form.volume.data
    item.description = form.description.data
    item.user = current_user.id

# Delete item from db
@app.route("/items/rm/<item_id>", methods=["POST"])
@login_required
def item_rm(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()

    return render_template("items/list.html", items = Item.query.all())