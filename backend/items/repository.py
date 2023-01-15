import uuid
from datetime import datetime

import ydb as ydb

from backend.common.repository import AbcRepository
from backend.items import models


class ItemRepository(AbcRepository):
    __TABLE_NAME = 'items'

    def __init__(self, endpoint: str, database: str):
        super().__init__(endpoint, database, self.__TABLE_NAME)
        self.connect()

    @staticmethod
    def _get_table_schema(session: ydb.Session) -> ydb.TableDescription:
        return (
            ydb.TableDescription()
            .with_column(ydb.Column('id', ydb.PrimitiveType.String))
            .with_column(ydb.Column('title', ydb.PrimitiveType.String))
            .with_column(ydb.Column('text', ydb.PrimitiveType.String))
            .with_column(ydb.Column('author', ydb.OptionalType(ydb.PrimitiveType.String)))
            .with_column(ydb.Column('created_at', ydb.PrimitiveType.Datetime))
            .with_primary_key('id')
        )

    @property
    def __table_name(self) -> str:
        return self.__TABLE_NAME

    def insert(self, model: models.AddItem) -> models.Item:
        def payload_func(session: ydb.Session):
            query = '''
            insert into {table} (id, title, text, author, created_at)
            values ("{id}", "{title}", "{text}", "{author}", DATETIME("{created_at}"));
            '''.format(
                table=self.__TABLE_NAME,
                id=uuid.uuid4(),
                **model.dict(),
                created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            )
            session.transaction().execute(query, commit_tx=True)
            return model
        return self._pool.retry_operation_sync(payload_func)

    def all(self) -> list[models.Item]:
        def payload_func(session: ydb.Session):
            result = []
            query = """select id, title, text, author, created_at from {}""".format(self.__TABLE_NAME)
            query_result = session.transaction().execute(query)
            for row in query_result[0].rows:
                result.append(models.Item.parse_obj(row))
            return result
        return self._pool.retry_operation_sync(payload_func)
