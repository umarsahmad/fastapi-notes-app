from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# In-memory storage for items
items = [{'id': 1, 'desc': 'sunny'}, 
         {'id': 2, 'desc': 'umar'}]

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float



# @app.get("/")
# async def read_root():
#     return {"message": "Hello, World"}

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = items
    return templates.TemplateResponse(
        "base.html", {'request': request, 'docs': items}
    )


# @app.get("/list")
# async def todoList():
#     return items

@app.post("/", response_class=HTMLResponse)
async def create_item(request: Request):
    form = await request.form()
    # print(dict(form))
    items.append(dict(form))
    return templates.TemplateResponse(
        "base.html", {'request': request, 'docs': items}
    )

@app.post("/del", response_class=HTMLResponse)
async def delete_item(request: Request):
    form = await request.form()
    # print(dict(form))
    key = dict(form).keys()

    idRemove = int(list(key)[0]) - 1

    items.pop(idRemove)

    return templates.TemplateResponse(
        "base.html", {'request': request, 'docs': items}
    )