from _typeshed import Incomplete
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.data_models.filter import Filter as Filter
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator, NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.utils import Q
from collections.abc import Callable as Callable
from datetime import date, datetime
from pydantic import BaseModel
from typing import Any, ClassVar

SUPPORTED_NESTED_FIELDS: Incomplete
ADDRESS_FIELD: str
METADATA_FIELD: str
MODEL_TABLE_ALIAS: str
METADATA_TABLE_ALIAS: str

class NoValue: ...

class SqlOperatorTemplate(BaseModel):
    """
    Represents a SQL operator template for building SQL statements and values.

    Attributes:
        template (str | Callable[[Any, str | None], str]): The template for the SQL statement.
        value_template (str | None): The template for the SQL value.
        value_modifier (Callable[[Any, str | None], Any] | None): A function to modify the SQL value.
    """
    build_statement: ClassVar[Callable[[Any, str, Any, str, str, str | None], str]]
    build_value: ClassVar[Callable[[Any, Any, str | None], Any]]
    template: str | Callable[[Any, str | None], str]
    value_template: str | None
    value_modifier: Callable[[Any, str | None], Any] | None
    def build_statement(self, field_name: str, value: Any, table_name: str = '', column_separator: str = "'", column_type: str | None = None) -> str:
        '''
        Builds the SQL statement for the given field and value.

        Args:
            field_name (str): The name of the field.
            value (Any): The value to be used in the statement.
            table_name (str, optional): The name of the table. Defaults to \'\'.
            column_separator (str, optional): The separator for the column. Defaults to "\'".
            column_type (str | None, optional): The type of the column. Defaults to None.

        Returns:
            str: The built SQL statement.
        '''
    def build_value(self, value: Any, column_type: str | None = None) -> Any:
        """
        Builds the SQL value for the given value.

        Args:
            value (Any): The value to be used in the statement.
            column_type (str | None, optional): The type of the column. Defaults to None.

        Returns:
            Any: The built SQL value.
        """

sql_operator_map: dict[Lookup, SqlOperatorTemplate]
METADATA_SELECT_STATEMENT: str
METADATA_SELECT_FIELD: Incomplete

class SqliteStatementsMixin:
    TABLE_SEPARATOR: str
    COLUMN_SEPARATOR: str
    SQL_OPERATOR_MAP: dict[Lookup, SqlOperatorTemplate]
    SUBSTITUTE_CHAR: str
    table_schema_manager: TableSchemaServiceBase
    def _fields_map(self, table_name: str, field_name: str, class_version: str | Versions) -> str: ...
    def _field_reverse_map(self, table_name: str, field_name: str, class_version: str | Versions) -> str: ...
    def _build_insert_statement(self, table_name: str, data: dict[str, Any]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_bulk_insert_statement(self, table_name: str, data: list[dict[str, Any]]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_delete_statement(self, table_name: str, data: dict[str, Any]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_bulk_delete_statement(self, table_name: str, data: list[dict[str, Any]]) -> tuple[str, tuple[Any, ...]]: ...
    def _build_select_statement(self, table_name: str, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None, *, use_internal_meta_tables: bool = False, select_related: dict[tuple[str, Address, str], Any] | None = None) -> tuple[str, list[Any]]: ...
    def _column(self, column_name: str) -> str: ...
    def _table(self, table_name: str) -> str: ...
    def _select_statement(self, table_name: str, select_only: str, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None, *, is_internal_table: bool = False, select_related: dict[tuple[str, Address, str], Any] | None = None) -> tuple[str, list[Any]]: ...
    def _nested_sub_select_related(self, select_related: dict[tuple[str, Address, str], Any]) -> list[str]: ...
    def _sub_column(self, sub_alias: str, field_name: str) -> str: ...
    def _build_join(self, parent_table_name: str, field_name: str, address: Address, alias: str, parent_alias: str, select_related: dict[tuple[str, Address, str], Any] | None = None) -> str: ...
    def _select_with_internal_meta_statement(self, table_name: str, select_only: str, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None, select_related: dict[tuple[str, Address, str], Any] | None = None) -> tuple[str, list[Any]]: ...
    def _build_count_statement(self, table_name: str, conditions: Q | None = None, *, use_internal_meta_tables: bool = False) -> tuple[str, list[Any]]: ...
    def _get_conditions_statement(self, table_name: str, conditions: Q, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False, is_grouped: bool = False) -> tuple[str, list[Any]]: ...
    def _get_filter_statement(self, table_name: str, filter_item: Filter, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> tuple[str, Any]: ...
    def _nested_filter_statement(self, table_name: str, field_name: str, nested_fields: str, sql_operator_template: SqlOperatorTemplate, value: Any, value_type: Any, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> tuple[str, Any]: ...
    def _resolve_nested_field_name(self, table_name: str, field_name: str, nested_fields: str, *, value_type: Any = ..., is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> str: ...
    def _build_order_by_statement(self, table_name: str, order_by: list[OrderBy] | None, *, is_internal_table: bool = False, use_internal_meta_tables: bool = False) -> str: ...
    @classmethod
    def _convert_date_to_sql_value(cls, value: date | datetime) -> int: ...
    @classmethod
    def _to_sql_value(cls, value: Any) -> Any: ...
    def _describe_table(self, table_name: str) -> dict[str, str]: ...
    def _process_result(self, table_name: str, result: dict[str, Any], table_description: dict[str, str], select_related: dict[tuple[str, Address, str], Any] | None = None) -> dict[str, Any]: ...
    @staticmethod
    def _process_field(field_type: str, value: Any) -> Any: ...
