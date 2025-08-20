from fastapi import FastAPI
import random as ran

app = FastAPI()

name_list = [
    {"id":1,"name":"ali"},
    {"id":2,"name":"maryam"},
    {"id":3,"name":"amir"},
    {"id":4,"name":"aziz"},
    {"id":5,"name":"zahra"}
]

@app.get("/")
def root():
    return {"massage":"hello amir"}

@app.get("/items/foo")
def root2():
    return {"massage":"hello amirali"}

@app.get("/names")
def ret_names_list():
    return name_list


@app.post("/names")
def create_name(name:str):
    name_obj = {"id":ran.randint(6,100),"name":name}
    name_list.append(name_obj)
    return name_obj

@app.get("/names/{name_id}") #http://127.0.0.1:8000/names/1
def ret_name_id(name_id:int):
    for name in name_list:
        if name["id"] == name_id:
            return name
    return {"پیام": f"نامی با شناسه {name_id} پیدا نشد"}

@app.put("/names/{name_id}")
def update_name(name_id:int,name:str):
    for item in name_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    return {"پیام": f"نامی با شناسه {name_id} پیدا نشد"}
        