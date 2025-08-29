from fastapi import FastAPI,Query,status,HTTPException,Path,Form,Body # body and ferm in json not in URL
from fastapi import UploadFile,File
import random as ran
from typing import Optional,Annotated,List
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


"""
@app.on_event("startup") # khat khorde chon masokh shode
def startup_event():
    print("stsrting the app")

@app.on_event("shutdown")
def shutting_down_event():
    print("shutting down the app ")
"""

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

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
    # return {"massage":"hello amir"}
    return JSONResponse(content={"message":"hello Amir"},status_code=status.HTTP_202_ACCEPTED)

@app.get("/items/foo")
def root2():
    # return {"massage":"hello amirali"}
    return JSONResponse(content={"message":"hello Amirali"},status_code=status.HTTP_202_ACCEPTED)


@app.get("/namesss")
def show_names_list():
    return name_list


# @app.post("/names")
@app.post("/names",status_code=status.HTTP_201_CREATED)
# def create_name(name:str):
# def create_name(name:str = Body()):
# def create_name(name:str = Body(),age:int = Body()):
def create_name(name:str = Body(embed=True)):
    name_obj = {"id":ran.randint(6,100),"name":name}
    name_list.append(name_obj)
    # return name_obj
    return JSONResponse(content=name_obj,status_code=status.HTTP_202_ACCEPTED)



@app.get("/names/{name_id}") #http://127.0.0.1:8000/names/1
def serch_name_id(name_id:int = Path(alias="serch",title="object id in name",description="the id of the name in name_list")):
    for name in name_list:
        if name["id"] == name_id:
            return name
    # return {"پیام": f"نامی با شناسه {name_id} پیدا نشد"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="objeckt not found")


# @app.put("/names/{name_id}")
@app.put("/names/{name_id}",status_code=status.HTTP_200_OK)
# def update_name(name_id:int,name:str):
def update_name(name_id:int = Path(),name:str = Form()):
    for item in name_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    # return {"پیام": f"نامی با شناسه {name_id} پیدا نشد"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="objeckt not found")


"""
# @app.delete("/names{name_id}")
@app.delete("/names{name_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_name(name_id:int):
    for itme in name_list:
        if itme["id"] == name_id:
            # name_list.remove({"id":itme["id"],"name":itme["name"]})
            name_list.remove(itme)
            return {"messga:sussec"}
    # return {"پیام": f"نامی با شناسه {name_id} پیدا نشد"}
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="objeckt not found")
"""
@app.delete("/names/{name_id}")
def delete_name(name_id:int):
    for itme in name_list:
        if itme["id"] == name_id:
            name_list.remove(itme)
            return JSONResponse(content={"messga":"object remove"},status_code=status.HTTP_202_ACCEPTED)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="objeckt not found")


"""
@app.get("/namesq")
# def cury_parametr(q:str | None = None): #24 t 26 comment
# def cury_parametr(q:Optional[str]): #24 t 26 comment
def cury_parametr(q: Annotated[str | None,Query(max_length=50)] = None):
    if q:
        serch_list = [item for item in name_list if item["name"]==q]
        if serch_list != []:
            return serch_list
        else:
            # return {"پیام": f"نامی با شناسه {q} پیدا نشد"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="objeckt not found")
    # else: # bejay none = none
        # return {"پیام": f"نامی با شناسه {q} پیدا نشد"}
"""
@app.get("/names")                                                                       #example="AMIR"        
def serch_to_name_list(q: str | None = Query(description="in sercher list",title="serch",alias="serch",default=None,max_length=50)):# redocs#
    if q:
        return [item for item in name_list if item["name"]==q]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="objeckt not found")
    

"""
@app.post("/upload_file/",status_code=status.HTTP_201_CREATED)
def upload_file(file: bytes = File(...)):
    print(file)
    # return {"file_size":len(file)}
    JSONResponse(content={"file_size":len(file)},status_code=status.HTTP_202_ACCEPTED)
"""
@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    print(file.__dict__)
    contentt = await file.read()
    # JSONResponse(content={"filename":file.filename,"file_type":file.content_type,"file_size":len(contentt)})
    return {"filename":file.filename,"file_type":file.content_type,"file_size":len(contentt)}


@app.post("/multipel_file/")
async def multipel_files(files : List[UploadFile]):
    return [{"filename":file.filename,"file_type":file.content_type} for file in files]


