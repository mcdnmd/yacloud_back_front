import datetime
import platform
import uuid


from backend.common.app import router
from fastapi import Request

from backend.items import models
from backend.items.repository import ItemRepository


@router.get('/items/')
def read_item(request: Request) -> list[models.Item]:
    item_repository: ItemRepository = request.app.item_repository
    return item_repository.all()


@router.post('/items/')
def read_item(request: Request, item: models.AddItem) -> models.Item:
    item_repository: ItemRepository = request.app.item_repository
    return item_repository.insert(item)


@router.get('/version/')
def get_version():
    with open(".back-version", "r") as f:
        return f.read(), platform.node()
