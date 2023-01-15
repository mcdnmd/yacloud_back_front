import abc

import ydb as ydb
from loguru import logger
from pydantic import BaseModel


class AbcRepository(abc.ABC):
    __TABLE_NAME = None

    def __init__(self, endpoint: str, database: str, table_name: str):
        self.__TABLE_NAME = table_name
        self._endpoint = endpoint
        self._database = database
        self._db_driver = ydb.Driver(endpoint=self._endpoint, database=self._database)
        self._pool: ydb.SessionPool | None = None

    def _prepare_db(self, session: ydb.Session) -> None:
        schema = self._get_table_schema(session)
        logger.info(self.__TABLE_NAME)
        logger.info(schema)
        # session.create_table(self.__TABLE_NAME, schema)

    def connect(self) -> None:
        self._db_driver.wait(timeout=5, fail_fast=True)
        self._pool = ydb.SessionPool(self._db_driver)
        self._pool.retry_operation_sync(self._prepare_db)
        self._pool.retry_operation_sync(self._prepare_db)

    def close(self) -> None:
        self._db_driver.stop(timeout=5)

    @staticmethod
    @abc.abstractmethod
    def _get_table_schema(session: ydb.Session) -> ydb.TableDescription:
        ...

    @abc.abstractmethod
    def insert(self, model: BaseModel) -> BaseModel:
        ...

    @abc.abstractmethod
    def all(self) -> list[BaseModel]:
        ...
