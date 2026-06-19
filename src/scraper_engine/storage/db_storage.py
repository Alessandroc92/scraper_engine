from collections.abc import Iterator
from contextlib import contextmanager
import logging
from typing import Any

from sqlalchemy import MetaData, Table, create_engine, Select, Insert, Update, Delete
from sqlalchemy.engine import Connection, Engine

from scraper_engine import loggers

loggers.create_dictconfig()
logger = logging.getLogger(__name__)


class DbStorage:
    def __init__(self, db_url: str, echo: bool = False):
        self.db_url = db_url
        self.echo = echo
        self.metadata = self.instantiate_metadata()
        self.engine = self.create_engine_instance()

    def instantiate_metadata(self):
        return MetaData()


    def create_engine_instance(self) -> Engine:
        engine = create_engine(url=self.db_url, echo=self.echo)
        return engine

    @contextmanager
    def create_transaction(self) -> Iterator[Connection]:
        try:
            with self.engine.begin() as conn:
                yield conn
        except Exception:
            logger.exception(
                "CRITICAL ERROR WHEN EXECUTING SQL STATEMENT",
            )
            raise

    def create_table(self, table_name: str, *args) -> Table:
        table = Table(table_name, self.metadata, *args)
        self.metadata.create_all(self.engine, tables=[table])
        return table

    def fetch_results(self, stmt: Select[Any]) -> list[dict[str, Any]]:
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return [dict_row for dict_row in result.mappings()]
        
    def execute_query(self, stmt: Insert | Update | Delete) -> int | None:
        with self.create_transaction() as conn:
            result = conn.execute(stmt)
            return getattr(result, 'rowcount', None)
        
    def drop_table(self, table: Table):
        return table.drop(self.engine, checkfirst=True)

