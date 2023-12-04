from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

# to run script, $ uvicorn path/<script without '.py'>:app --reload

app = FastAPI()


class Item(BaseModel):
    # BaseModel turns passed data into a JSON
    name: str
    value: Optional[float] = None
    active_trade: bool


class UpdateItem(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    active_trade: Optional[bool] = None


# mock JSON inventory
# inventory = {
#     1: {
#         "name": "unique_name",
#         "value": 12.345,
#         "active_trade": True
#     }
# }
inventory = {}


# set up home endpoint
@app.get("/")
def home():
    return {"Data": "Test"}


# GET by path
@app.get("/get-item/{item_id}/")
def get_item_by_id(item_id: int = Path(description="The ID of the respective inventory item", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="404: Item ID not found")
    return inventory[item_id]


# GET by query
@app.get("/get-by-name")
# /get-by-name?name=<name>
def get_item_by_name(name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="404: Item name not found")


# POST new item
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=404, detail="400: Item ID already exists")
    # item inherits from BaseModel, so it's automatically turned into a JSON
    inventory[item_id] = item
    return inventory[item_id]


# PUT for updating item
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="404: Item ID not found")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.value != None:
        inventory[item_id].value = item.value

    if item.active_trade != None:
        inventory[item_id].active_trade = item.active_trade

    return inventory[item_id]

# DELETE item
@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="404: Item ID not found")
    del inventory[item_id]
    return {"Success": "It's a distant memory"}