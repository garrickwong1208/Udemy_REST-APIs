from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99        
            }
        ]
    }
]



#Get a dictionary of all stores 
@app.get("/store")    #http://127.0.0.1:5000/store
def get_stores():
    return {"stores": stores}


#Post a new store with no items
@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201   # 200 means success, 201 means accepted change    

#Post a new item in specific store
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201

    return {"message": "Store not found"}, 404 # common error message

#Get store info of specific store
@app.get("/store/<string:name>")    
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

#Get items in specific store
@app.get("/store/<string:name>/item")    
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
