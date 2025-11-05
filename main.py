# main.py
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello World from FastAPI on Vercel!"}

# @app.get("/api/health")
# def health_check():
#     return {"status": "healthy"}

# # This is important for Vercel
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

import os
from fastapi import FastAPI
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, Text, create_engine, select

from models.apimodels import BPApiSchema, ItemID
from models.pagemodels import BPPageSchema, PageItemID
from fastapi.middleware.cors import CORSMiddleware

"""
clientID,appId,apiname,apischema

"""


## TODO 1 : 1 create a DatabaseConnectionUrl variable
# DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/build_perfect'
# DATABASE_URL = 'postgresql://postgres:postgres@192.168.0.172:5432/postgres'
# DATABASE_URL = 'postgresql://neondb_owner:npg_x7sCnUzQW0iM@ep-curly-scene-a4fstp5c-pooler.us-east-1.aws.neon.tech/buildperfect?sslmode=require&channel_binding=require'
DATABASE_URL = os.environ["DATABASE_URL"]
## TODO 2 - create engine 

engine = create_engine(DATABASE_URL,echo=True)

# TODO 3 - create database and table 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# TODO 4 - Dependency to get DB session and session used for db transanction

def get_session():
    with Session(engine) as session:
        yield session

# TODO 5 - create reference for Session 

SessionDep = Annotated[Session,Depends(get_session)]

# SQLModel for both database and Pydantic


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## create db and table on startup of the server
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}

############### APIBuilder API ROUTES #########################


## post endpoint for saving BPApiSchema

@app.post("/api/saveApiSchema/",response_model=BPApiSchema)
def saveApiSchema( apiSchema:BPApiSchema , session : SessionDep):
    session.add(apiSchema)
    session.commit()
    session.refresh(apiSchema)
    return apiSchema

## get api for get all saved apiSchema

@app.post("/api/getAllApiSchema/",response_model=list[BPApiSchema])
def getAllAPiSchema(session:SessionDep):
    apis = session.exec(select(BPApiSchema)).all()
    return apis

## 

@app.post("/api/getApiSchemaById/",response_model=BPApiSchema)
def getApiSchemaById(id:ItemID,session:SessionDep):
       statement = select(BPApiSchema).where(BPApiSchema.apiId == id.id)
       session_user = session.exec(statement).first()
       return session_user

############### PAGES API ROUTES #########################

## post endpoint for saving pages BPPageSchema

@app.post("/api/savePageSchema/",response_model=BPPageSchema)
def saveApiSchema( apiSchema:BPPageSchema , session : SessionDep):
    session.add(apiSchema)
    session.commit()
    session.refresh(apiSchema)
    return apiSchema

## get api for get all saved apiSchema

@app.post("/api/getAllPagesSchema/",response_model=list[BPPageSchema])
def getAllAPiSchema(id:ItemID,session:SessionDep):
    pages = session.exec(select(BPPageSchema).where(BPPageSchema.appId == id.id)).all()
    return pages

## 

@app.post("/api/getPageSchemaById/",response_model=BPPageSchema)
def getApiSchemaById(id:PageItemID,session:SessionDep):
       statement = select(BPPageSchema).where(BPPageSchema.pageId == id.id)
       session_user = session.exec(statement).first()
       print(session_user)
       return session_user

## update a page 

@app.post("/api/updatePage/")
def updatePageDetails(id:PageItemID,session:SessionDep):
     page_db = session.get(BPPageSchema,id.id)
     if not page_db:
          raise HTTPException(status_code=404,detail="Page Not Found")
     
## delete a page by pageID

# @app.delete("/api/deletePage")
# def deletePage(id:PageItemID,session:SessionDep):
#      page = session.get(BPPageSchema,id.id)
#      if not page:
#           raise HTTPException(status_code=404,detail="Page Not Found")
#      session.delete(page)
#      session.commit()
#      return {"ok":True}

## update a page by pageID


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)