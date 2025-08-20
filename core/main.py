from fastapi import FastAPI,Query
import random as ran
from typing import Optional,Annotated

app = FastAPI()

name_list = [
    {"id":1,"name":"ali"},
    {"id":2,"name":"maryam"},
    {"id":3,"name":"amir"},
    {"id":4,"name":"aziz"},
    {"id":5,"name":"zahra"},
    {"id":6,"name":"ali"},
    {"id":7,"name":"ali"}
]

@app.get("/")
def root():
    return {"massage":"hello amir"}

@app.get("/items/foo")
def root2():
    return {"massage":"hello amirali"}

# @app.get("/names")
# def ret_names_list():
#     return name_list


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

@app.delete("/names{name_id}")
def delete_name(name_id:int):
    for itme in name_list:
        if itme["id"] == name_id:
            # name_list.remove({"id":itme["id"],"name":itme["name"]})
            name_list.remove(itme)
            return {"messga:sussec"}
    return {"پیام": f"نامی با شناسه {name_id} پیدا نشد"}


@app.get("/names")
# def cury_parametr(q:str | None = None): #24 t 26 comment
# def cury_parametr(q:Optional[str]): #24 t 26 comment
def cury_parametr(q: Annotated[str | None,Query(max_length=50)]=None):
    if q:
        serch_list = [item for item in name_list if item["name"]==q]
        if serch_list != []:
            return serch_list
        else:
            return {"پیام": f"نامی با شناسه {q} پیدا نشد"}
    # else: # bejay none = none
    #     return {"پیام": f"نامی با شناسه {q} پیدا نشد"}
