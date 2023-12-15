from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import json

from pydantic import BaseModel

import pymongo

import uvicorn

client = pymongo.MongoClient('mongodb://sam9:sam9mo!!@59.3.28.12:27017/')
db = client["sam9mo"]
collection = db["favorite_stock"]

class ReceiveItem(BaseModel):
    account :str
    
class SendItem(BaseModel):
    account :str
    favorite_stock :list
    
class AddItem(BaseModel):
    account :str
    favorite_stock :dict
    
class RemoveItem(BaseModel):
    account :str
    favorite_stock :str

class UpdateItem(BaseModel):
    account :str
    favorite_stock :str
    fluctuation :float
    fluctuation_toggle : str

def onStartUp():
    print('server start')
    
def onShutDown():
    print('server disconnected')
    
def get_favorite_stock(userEmail):
    find_query = {
        "account" : userEmail
    }
    result = collection.find_one(find_query)
    
    send_data = {
        "favorite_stock" : result["favorite_stock"]
    }
    
    return send_data

def insert_favorite_stock(item :SendItem):
    update_query = {
        "account" : item.account,
        "favorite_stock" : item.favorite_stock
    }
    try:
        collection.insert_one(update_query)
        send_data = {
            "status" : "success"
        }
    except:
        send_data = {
            "status" : "Fail"
        }
    return send_data

def add_favorite_stock(item :AddItem):
    find_query = {
        "account" : item.account
    }
    
    update_query = {
        
        "$addToSet": {"favorite_stock": {"$each": [item.favorite_stock]}}
    }
    try:
        collection.update_one(find_query, update_query)
        document = collection.find_one(find_query)
        send_data = {
            "status" : "success",
            "data" : {
                "account" : document["account"],
                "favorite_stock" : document["favorite_stock"]
            }
        }
    except:
        send_data = {
            "status" : "Fail"
        }
    return send_data

def remove_favorite_stock(item :RemoveItem):
    find_query = {
        "account" : item.account
    }
    update_query = {
        "$pull": {
            "favorite_stock": 
                {item.favorite_stock : {"$exists": True}}
        }
    }
    try:
        collection.update_one(find_query, update_query)
        document = collection.find_one(find_query)
        send_data = {
            "status" : "success",
            "data" : {
                "account" : document["account"],
                "favorite_stock" : document["favorite_stock"]
            }
        }
    except:
        send_data = {
            "status" : "Fail"
        }
    return send_data

def update_favorite_stock(item :UpdateItem):
    find_query = {
        "account" : item.account,
        f'favorite_stock.{item.favorite_stock}' : {
            "$exists" : True
        }
    }
    update_query = {
        "$set": {
            f'favorite_stock.$[elem].{item.favorite_stock}.fluctuation' : item.fluctuation,
            f'favorite_stock.$[elem].{item.favorite_stock}.fluctuation_toggle' : item.fluctuation_toggle
        }
    }
    
    array_filters = [{f'elem.{item.favorite_stock}': {"$exists": True}}]
    
    try:
        collection.update_one(find_query, update_query, array_filters=array_filters)
        document = collection.find_one(find_query)
        send_data = {
            "status" : "success",
            "data" : {
                "account" : document["account"],
                "favorite_stock" : document["favorite_stock"]
            }
        }
    except Exception as ex:
        send_data = {
            "status" : f'Fail {ex}'
        }
    return send_data
    
app = FastAPI(on_startup=[onStartUp], on_shutdown=[onShutDown])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    path="/favorite_stock/receive"
)
def favorite_stock_receive(item :ReceiveItem):
    return get_favorite_stock(item.account)

@app.post(
    path="/favorite_stock/send"
)
def favorite_stock_send(item :SendItem):
    return insert_favorite_stock(item)

@app.post(
    path="/favorite_stock/add"
)
def favorite_stock_add(item :AddItem):
    print("item", item, type(item.favorite_stock))
    return add_favorite_stock(item)

@app.post(
    path="/favorite_stock/remove"
)
def favorite_stock_remove(item :RemoveItem):
    return remove_favorite_stock(item)

@app.post(
    path="/favorite_stock/update"
)
def favorite_stock_update(item :UpdateItem):
    print(update_favorite_stock(item))
    return update_favorite_stock(item)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8096)
