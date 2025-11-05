from sqlmodel import Column, Field, SQLModel, Text
from pydantic import BaseModel


"""
save API details to db 
field
    clientId        |   str
    clientName      |   str
    appId           |   str
    appName         |   str
    apiName         |   str
    apiId           |   primarykey
    apiStatus       |   boolean
    schema          |   text  
"""
class BPApiSchema(SQLModel, table=True):
    clientId:str    = Field(index=True)
    clientName:str  = Field(index=True)
    appId:str       = Field(index=True)
    appName:str     = Field(index=True)
    apiName:str     = Field(index=True)
    apiId:str       = Field(primary_key=True,index=True)
    apiStatus:bool
    schema:str      = Field(sa_column=Column(Text))

class ItemID(BaseModel):
    id:str


class BPApiSchemaUpdate(SQLModel):
    clientId:str    | None
    clientName:str  | None
    appId:str       | None
    appName:str     | None
    apiName:str     | None
    apiId:str       | None
    apiStatus:bool  | None
    schema:str      | None