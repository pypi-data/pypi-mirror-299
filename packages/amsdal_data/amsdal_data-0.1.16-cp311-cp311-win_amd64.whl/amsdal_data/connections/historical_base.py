from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_utils.models.data_models.address import Address

from amsdal_data.connections.base import ConnectionBase


class HistoricalConnectionBase(ConnectionBase, ABC):
    @abstractmethod
    def put(self, address: Address, data: dict[str, Any]) -> None:
        """
        Adds/writes data to in scope of transaction.

        Args:
            address (Address): The address of the object.
            data (dict[str, Any]): The object data to write.

        Returns:
            None
        """
        ...

    @abstractmethod
    def bulk_put(self, data: list[tuple[Address, dict[str, Any]]]) -> None:
        """
        Adds/writes data to in scope of transaction.

        Args:
            address (Address): The address of the object.
            data (list[dict[str, Any]]): The object data to write.

        Returns:
            None
        """
        ...
