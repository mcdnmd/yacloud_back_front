import datetime
import uuid

from pydantic import BaseModel


class Item(BaseModel):
    id: uuid.UUID
    title: str
    text: str
    author: str
    created_at: datetime.datetime


class AddItem(BaseModel):
    title: str
    text: str
    author: str

