from abc import ABC
from abc import abstractmethod

from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableSchema

from amsdal_data.connections.base import ConnectionBase


class TableSchemaServiceBase(ABC):
    def __init__(self, connection: ConnectionBase):
        self.connection = connection

    @abstractmethod
    def register_table(self, table_schema: TableSchema) -> tuple[str, bool]:
        """
        Creates a table in the database and returns the table name and flag indicating if the table was created
            or updated.

        This method checks if a table with the specified schema already exists in the database.
        If the table exists, it updates the table schema. If the table does not exist, it creates
        the table and its indexes.

        Args:
            table_schema (TableSchema): The schema definition for the table to register.

        Returns:
            tuple[str, bool]: A tuple containing the table name and a boolean indicating whether
            the table was created (True) or updated (False).
        """
        ...

    @abstractmethod
    def unregister_table(self, address: Address) -> None:
        """
        Unregister a table in the database.

        Returns:
            None
        """
        ...

    @abstractmethod
    def resolve_table_name(self, address: Address) -> str: ...

    @abstractmethod
    def register_internal_tables(self) -> None: ...

    @abstractmethod
    def update_internal_table(self, table_schema: TableSchema) -> None: ...
