import logging
import uuid
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import Union

from amsdal_data.connections.base import ConnectionBase
from amsdal_data.manager import AmsdalDataManager
from amsdal_utils.classes.version_manager import ClassVersionManager
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.data_models.address import Address

if TYPE_CHECKING:
    from amsdal_models.querysets.base_queryset import ModelType
    from amsdal_models.querysets.base_queryset import QuerySetBase

logger = logging.getLogger(__name__)

DEFAULT_DB_ALIAS = 'default'
LAKEHOUSE_DB_ALIAS = 'lakehouse'


class ExecutorBase(ABC):
    """
    Abstract base class for query executors.

    This class provides the base functionality for executing queries and counting
    results. It defines the interface that all concrete executor classes must implement.

    Attributes:
        queryset (QuerySetBase): The query set to be executed.
    """

    queryset: 'QuerySetBase'

    def __init__(self, queryset: 'QuerySetBase') -> None:
        self.queryset = queryset
        self._config_manager = AmsdalConfigManager()

    def _get_connection_name(self) -> str:
        if self.queryset._using == DEFAULT_DB_ALIAS:
            return self._config_manager.get_connection_name_by_model_name(self.queryset.entity_name)

        if self.queryset._using == LAKEHOUSE_DB_ALIAS:
            return self._config_manager.get_config().resources_config.lakehouse

        return self.queryset._using

    def _get_connection(self) -> ConnectionBase:
        return AmsdalDataManager().get_connection_manager().get_connection(self._get_connection_name())

    @abstractmethod
    def query(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def count(self) -> int: ...


class Executor(ExecutorBase):
    """
    Concrete executor class for executing queries and counting results.

    This class extends the `ExecutorBase` and provides the implementation for
    executing queries and counting results using the specified query set.
    """

    def _address(self) -> Address:
        return Address(
            resource='',
            class_name=self.queryset.entity_name,
            class_version=ClassVersionManager().get_latest_class_version(self.queryset.entity_name).version,
            object_id='',
            object_version='',
        )

    def query(self) -> list[dict[str, Any]]:
        """
        Execute the query and return the results.

        This method uses the connection object to execute the query based on the
        query set's specifier, conditions, pagination, and order by attributes.

        Returns:
            list[dict[str, Any]]: The query results as a list of dictionaries.
        """
        _select_related = None
        if isinstance(self.queryset._select_related, dict):
            _select_related = self._process_select_related(self.queryset._select_related, self.queryset._entity)

        return self._get_connection().query(
            address=self._address(),
            query_specifier=self.queryset._query_specifier,
            conditions=self.queryset._conditions,
            pagination=self.queryset._paginator,
            order_by=self.queryset._order_by,
            select_related=_select_related,
        )

    def _process_select_related(
        self,
        select_related: dict[str, Any],
        model: type['ModelType'],
    ) -> dict[tuple[str, Address, str], Any]:
        from amsdal_models.classes.model import LegacyModel
        from amsdal_models.classes.model import Model

        _select_related = {}

        for key, value in select_related.items():
            _field_type = model.model_fields[key].annotation

            if not _field_type or not hasattr(_field_type, '__origin__') or _field_type.__origin__ != Union:
                msg = 'Select related field must be a Union type'
                raise ValueError(msg)

            base_class: type[Model] | None = next(
                (arg for arg in _field_type.__args__ if issubclass(arg, Model) and not issubclass(arg, LegacyModel)),
                None,
            )
            if not base_class:
                msg = 'Select related field must be a Model type'
                raise ValueError(msg)

            _related = self._process_select_related(value, base_class)
            for version in ClassVersionManager().get_class_versions(base_class.__name__):
                _select_related[
                    (
                        key,
                        Address(
                            resource='',
                            class_name=base_class.__name__,
                            class_version=version.version,
                            object_id='',
                            object_version='',
                        ),
                        't' + uuid.uuid4().hex[:8],
                    )
                ] = _related

        return _select_related

    def count(self) -> int:
        """
        Execute the query and return the count of results.

        This method uses the connection object to execute the query and return
        the count of model instances that match the query conditions.

        Returns:
            int: The count of matching results.
        """
        return self._get_connection().count(
            address=self._address(),
            conditions=self.queryset._conditions,
        )
