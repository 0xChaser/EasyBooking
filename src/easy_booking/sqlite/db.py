import uuid

from sqlalchemy import String, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID


class SQLiteUUID(TypeDecorator):
    """
    Class to avoid UUID Problem with SQLite.
    """

    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        if dialect.name == "sqlite":
            if isinstance(value, uuid.UUID):
                return str(value)
            return str(value)
        if isinstance(value, str):
            return uuid.UUID(value)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        if dialect.name == "sqlite":
            if isinstance(value, str):
                return uuid.UUID(value)
            return value
        return value

    def process_literal_param(self, value, dialect):
        """Process literal values (used in SQL compilation)."""
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return str(value)
        return str(value)

    @property
    def python_type(self):
        return uuid.UUID