from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="${project_name}")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int = 1


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to ${project_name}"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/items")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict[str, int | str]:
    return {"item_id": item_id, "name": f"Item {item_id}"}