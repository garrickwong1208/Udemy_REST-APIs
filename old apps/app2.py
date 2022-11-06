import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores


app = Flask(__name__)

# stores = {
#   "b1dba70fda574cbcbead7b6a53d4bcd4" : 
#       {
#       "id": "b1dba70fda574cbcbead7b6a53d4bcd4",
#	    "name": "My Store"
#       } 
# }
# items = {
#     "fnasjkfneasjfn" : 
#         {
#         "name": "Chair",
#         "price": 17.99,
#         "store_id": "jcdnsakjfnsjfnjfn"
#         "id": "fnasjkfneasjfn"
#          },
#     "hkgremsgmgskgf" :
#         {
#         "name": "Table",
#         "price": 180.50,
#         "store_id": "fkekwafnknfkeasnf"
#         "id": "hkgremsgmgskgf"
#         }
# }


###################################       Stores       #############################################

#Get a dictionary of all stores 
@app.get("/store")    #http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}

#Get store info of specific store
@app.get("/store/<string:store_id>")    
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


#Post a new store with no items
@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload."
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201   # 200 means success, 201 means accepted change    

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try: 
        del stores[store_id]
        return { "message" : "Store deleted."}
    except KeyError:
        abort(404, message = "Store not found.")



###################################      Items       ################################################

#Get all items from ALL stores
@app.get("/item") 
def get_all_items():
    return {"items": list(items.values())}

#Get items under specific item id
@app.get("/item/<string:item_id>")    
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")

#Post a new item in specific store
@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here not only do we need to validate data exists,
    # But also what type of data. Price should be a float,
    # for example.
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message = "Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload"
        )
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")
    
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")  # no need to return because "abort" from smorest will take care of that

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201

#Delete item by using item_id
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try: 
        del items[item_id]
        return { "message" : "Item deleted."}
    except KeyError:
        abort(404, message = "Item not found.")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")

    try:
        item = items[item_id]   
        item |= item_data # updates existing dictionary; takes dict from left and replaces values from the rightside's dict

        return item
    except:
        abort(404, message="Item not found.")
    

