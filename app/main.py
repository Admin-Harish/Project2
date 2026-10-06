from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, Field

app = FastAPI(title="Project2 Inventory API", version="1.0.0")

items: dict[int, dict] = {}
next_id = 1


class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    quantity: int = Field(default=0, ge=0)


class ItemUpdate(BaseModel):
    quantity: int = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok", "service": "project2"}


@app.get("/api/items")
def list_items(q: str | None = Query(default=None, description="Filter by name substring")):
    found = [i for i in items.values() if not q or q.lower() in i["name"].lower()]
    return {"items": found, "count": len(found)}


@app.post("/api/items", status_code=201)
def create_item(item: ItemIn):
    global next_id
    if any(i["name"].lower() == item.name.lower() for i in items.values()):
        raise HTTPException(status_code=409, detail=f"Item '{item.name}' already exists")
    record = {"id": next_id, "name": item.name, "quantity": item.quantity, "in_stock": item.quantity > 0}
    items[next_id] = record
    next_id += 1
    return record


@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.put("/api/items/{item_id}")
def update_item(item_id: int, body: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id].update(quantity=body.quantity, in_stock=body.quantity > 0)
    return items[item_id]


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if items.pop(item_id, None) is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(status_code=204)
