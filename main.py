from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    content: str


@app.get("/")
def read_root():
    print("Hello from pi-security-camera!")


@app.get("/data")
def read_all_data() -> list[Item]:
    data: list[Item] = []
    with open("data/data.txt", "r") as file:
        dataline: list[str] = file.readline().split()
        data_item = {"content": dataline[1]}
        data.append(Item(**data_item))
    return data


@app.get("/data/{item_id}")
def read_item(item_id: int) -> Item:
    data_list: dict[int, Item] = {}
    with open("data/data.txt", "r") as file:
        dataline: list[str] = file.readline().split(",")
        data_item = {"content": dataline[1]}
        read_item_id: int = int(dataline[0])
        data_list[read_item_id] = Item(**data_item)

    if data_list.get(item_id) is None:
        raise HTTPException(status_code=404, detail="Item not found!")
    return data_list[item_id]


@app.put("/data/{item_id}")
def add_item(item_id: int, item: Item):
    with open("data/data.txt", "a") as file:
        _ = file.write(f"{item_id}, {item.content}")
    return {"item_id": item_id, "item_content": item.content}
