
import uvicorn
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from backend import config
from backend.common.app import app, router
from backend.items.repository import ItemRepository


def warm_up():
    """Общий прогрев приложения"""
    logger.info("Starting warm_up")
    item_repository = ItemRepository(endpoint=config.DB_ENDPOINT, database=config.DB_PATH)
    app.item_repository = item_repository
    logger.debug("Repository started")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.debug("Middleware added")

    app.include_router(router=router)
    logger.debug("Router added")


if __name__ == "__main__":
    warm_up()
    logger.info('Start app')
    uvicorn.run(app, host=config.HOST, port=config.PORT)
