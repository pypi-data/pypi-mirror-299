import abc
from abc import ABC, abstractmethod
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator as CursorPaginator, NumberPaginator as NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.utils import Q as Q
from typing import Any

class Connectable(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Connects to the database.

        Args:
            kwargs (Any): The connection parameters.

        Returns:
            None
        """
    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnects from the database.

        Returns:
            None
        """
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Checks if the connection is established.

        Returns:
            bool: True if connected, False otherwise.
        """
    @property
    @abstractmethod
    def is_alive(self) -> bool:
        """
        Checks if the connection is alive.

        Returns:
            bool: True if alive, False otherwise.
        """

class ConnectionBase(Connectable, ABC, metaclass=abc.ABCMeta):
    debug_mode: bool
    @abstractmethod
    def begin(self) -> None:
        """
        Begins a kind of transaction for this connection.

        Returns:
            None
        """
    @abstractmethod
    def commit(self) -> None:
        """
        Commits (stores) the objects to the database.

        Returns:
            None
        """
    @abstractmethod
    def revert(self) -> None:
        """
        Reverts the committed data.

        Returns:
            None
        """
    @abstractmethod
    def on_transaction_complete(self) -> None:
        """
        Called when the transaction is complete for all connections successfully.

        You should not write to the database in this method.

        Returns:
            None
        """
    @abstractmethod
    def rollback(self) -> None:
        """
        Rolls back the transaction itself.

        Returns:
            None
        """
    @abstractmethod
    def query(self, address: Address, query_specifier: QuerySpecifier | None = None, conditions: Q | None = None, pagination: NumberPaginator | CursorPaginator | None = None, order_by: list[OrderBy] | None = None, select_related: dict[tuple[str, Address, str], Any] | None = None) -> list[dict[str, Any]]:
        """
        Queries the database for objects.

        Args:
            address (Address): The address of the objects.
            query_specifier (QuerySpecifier | None): The query specifier that allows specifying the fields to return
                and the distinct fields.
            conditions (Q | None): The conditions to filter the objects by.
            pagination (NumberPaginator | CursorPaginator | None): The pagination object to paginate the objects.
            order_by (list[OrderBy] | None): The order by object to order the objects.

        Returns:
            list[dict[str, Any]]: List of objects data.
        """
    @abstractmethod
    def count(self, address: Address, conditions: Q | None = None) -> int:
        """
        Returns the count of objects in the database.

        Args:
            address (Address): The address of the objects.
            conditions (Q | None): The conditions to filter the objects by.

        Returns:
            int: Number of objects.
        """
    @property
    @abstractmethod
    def table_schema_manager(self) -> TableSchemaServiceBase:
        """
        Returns the table schema manager related to this type of connection.

        Returns:
            TableSchemaServiceBase: The table schema manager.
        """
    @abstractmethod
    def prepare_connection(self) -> None:
        """
        Ensures all the necessary system entities are created.

        Returns:
            None
        """
    @property
    def debug_queries(self) -> bool:
        """
        Returns the debug queries flag.

        Returns:
            bool: True if debug queries are enabled, False otherwise.
        """
    @property
    @abstractmethod
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
