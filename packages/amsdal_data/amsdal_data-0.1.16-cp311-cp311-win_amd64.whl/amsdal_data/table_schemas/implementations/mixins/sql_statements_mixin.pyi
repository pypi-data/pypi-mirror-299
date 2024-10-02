from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_data.table_schemas.data_models.sql_table_column import SqlTableColumn as SqlTableColumn, SqlTableColumnsSchema as SqlTableColumnsSchema
from amsdal_utils.models.data_models.table_schema import TableSchema as TableSchema
from typing import Any

class SqlStatementsMixin:
    """
    A mixin class that provides methods to build SQL statements for table operations.

    Attributes:
        TABLE_SEPARATOR (str): The character used to separate table names in SQL statements.
        COLUMN_SEPARATOR (str): The character used to separate column names in SQL statements.
    """
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    def _build_create_table_statement(self, table_name: str, table_schema: TableSchema, *, is_internal_table: bool = False, is_historical_table: bool = False) -> str: ...
    def _build_create_index_statement(self, table_name: str, index_name: str, columns: list[str]) -> str: ...
    def _build_update_table_statements(self, table_name: str, table_schema: TableSchema, table_columns: list[SqlTableColumn], *, is_internal_table: bool = False, is_historical_table: bool = False) -> list[str]: ...
    def _build_drop_table_statement(self, table_name: str) -> str: ...
    def _build_columns_from_schema(self, table_schema: TableSchema, *, is_internal_table: bool = False, is_historical_table: bool = False) -> list[SqlTableColumn]: ...
    @staticmethod
    def _build_constraints_from_schema(table_schema: TableSchema) -> list[str]: ...
    @staticmethod
    def _to_sql_type(type_: Any) -> str: ...
