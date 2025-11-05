from sqlmodel import Column, Field, SQLModel, Text
from pydantic import BaseModel


"""
save API details to db 
field
    clientId        |   str
    clientName      |   str
    appId           |   str
    appName         |   str
    pageName        |   str
    pageId          |   primarykey
    pageDescription |   str
    schema          |   text  
"""
class BPPageSchema(SQLModel, table=True):
    clientId:str    = Field(index=True)
    clientName:str  = Field(index=True)
    appId:str       = Field(index=True)
    appName:str     = Field(index=True)
    pageName:str     = Field(index=True)
    pageId:str       = Field(index=True,primary_key=True)
    pageDesc:str
    schema:str      = Field(sa_column=Column(Text))

class PageItemID(BaseModel):
    id:str

""""""
