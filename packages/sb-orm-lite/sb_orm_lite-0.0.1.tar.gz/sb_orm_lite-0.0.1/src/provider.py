import datetime
import re
from typing import List

from mapped_field import Mapped, FieldType, Integer, String, Float, DateTime, Decimal


class Provider(object):
    def escape_name(self, name: str) -> str:
        raise NotImplementedError()

    def escape_parameter(self, name: str) -> str:
        raise NotImplementedError()

    def build_create_field(self, field: Mapped) -> str:
        raise NotImplementedError()

    def build_create_table(self, fields: List[Mapped], table_name: str):
        raise NotImplementedError()

    def get_field_type(self, field_type: type) -> str:
        raise NotImplementedError()

    def get_optional_field(self, optional: bool) -> str:
        raise NotImplementedError()

    def get_is_primary_key(self, primary_key: bool) -> str:
        raise NotImplementedError()

    def get_autoincrement(self, autoincrement: bool) -> str:
        raise NotImplementedError()


class SqliteProvider(Provider):
    def escape_name(self, name: str) -> str:
        return "\"" + name + "\""

    def escape_parameter(self, name: str) -> str:
        return f":{name}"

    def build_create_field(self, field: Mapped) -> str:
        result = f"{self.escape_name(field.field_name)} {self.get_field_type(field.field_type)} {self.get_optional_field(field.optional)} {self.get_autoincrement(field.auto_increment)}"
        return result

    def build_create_table(self, fields: List[Mapped], table_name: str):
        result = f"CREATE TABLE {self.escape_name(table_name)} ("
        field_sql = []
        for field in fields:
            field_sql.append(self.build_create_field(field))

        pk_fields = [self.escape_name(f.field_name) for f in fields if f.primary_key]
        if len(pk_fields) > 0:
            field_sql.append(f"PRIMARY KEY ({', '.join(pk_fields)})")

        result += ", ".join(field_sql)
        result += ");"
        return result

    def get_field_type(self, field_type: FieldType) -> str:
        if isinstance(field_type, Integer):
            return "INTEGER"
        elif isinstance(field_type, String):
            return "TEXT"
        elif isinstance(field_type, Float) or isinstance(field_type, Decimal):
            return "NUMBER"
        elif field_type is DateTime:
            return "INTEGER"

    def get_optional_field(self, optional: bool) -> str:
        if optional:
            return "NULL"
        else:
            return "NOT NULL"

    def get_is_primary_key(self, primary_key: bool) -> str:
        if primary_key:
            return "PRIMARY KEY"
        else:
            return ""

    def get_autoincrement(self, autoincrement: bool) -> str:
        if autoincrement:
            return "AUTOINCREMENT"
        else:
            return ""


class MySqlProvider(Provider):
    def escape_name(self, name: str) -> str:
        return "`" + name + "`"

    def escape_parameter(self, name: str) -> str:
        return f"%({name})s"

    def build_create_field(self, field: Mapped) -> str:
        result = f"{self.escape_name(field.field_name)} {self.get_field_type(field_type)} {self.get_optional_field(optional)} {self.get_is_primary_key(primary_key)} {self.get_autoincrement(auto_increment)}"
        return result

    def get_field_type(self, field_type: type) -> str:
        if field_type is int:
            return "INT"
        elif field_type is str:
            return f"VARCHAR({50})"  # bit of a problem here
        elif field_type is float:
            return "FLOAT"
        elif field_type is datetime.datetime:
            return "DATETIME"

    def get_optional_field(self, optional: bool) -> str:
        if optional:
            return "NULL"
        else:
            return "NOT NULL"

    def get_is_primary_key(self, primary_key: bool) -> str:
        if primary_key:
            return "PRIMARY KEY"
        else:
            return ""

    def get_autoincrement(self, autoincrement: bool) -> str:
        if autoincrement:
            return "AUTO_INCREMENT"
        else:
            return ""


class PgSqlProvider(Provider):
    def escape_name(self, name: str) -> str:
        return "`" + name + "`"

    def escape_parameter(self, name: str) -> str:
        return f"%({name})s"

    def build_create_field(self, field: Mapped) -> str:
        result = f"{self.escape_name(field_name)} {self.get_field_type(field_type)} {self.get_optional_field(optional)} {self.get_is_primary_key(primary_key)} {self.get_autoincrement(auto_increment)}"
        return result

    def get_field_type(self, field_type: type) -> str:
        if field_type is int:
            return "INT"
        elif field_type is str:
            return f"VARCHAR({50})"  # bit of a problem
        elif field_type is float:
            return "FLOAT"
        elif field_type is datetime.datetime:
            return "DATETIME"

    def get_optional_field(self, optional: bool) -> str:
        if optional:
            return "NULL"
        else:
            return "NOT NULL"

    def get_is_primary_key(self, primary_key: bool) -> str:
        if primary_key:
            return "PRIMARY KEY"
        else:
            return ""

    def get_autoincrement(self, autoincrement: bool) -> str:
        if autoincrement:
            return "GENERATED ALWAYS AS IDENTITY"
        else:
            return ""


class ProviderFactory(object):
    @classmethod
    def get_provider(cls, connection_string: str) -> Provider:
        match = re.search(r"(\w+):\/\/(.+)", connection_string)
        if match:
            db_type = match.group(1)
            connection = match.group(2)

            if db_type == "sqlite":
                return SqliteProvider()
            elif db_type == "mysql":
                return MySqlProvider()
            elif db_type == "pgsql":
                return PgSqlProvider()

    @classmethod
    def get_provider_by_name(cls, db_type: str) -> Provider:
        if db_type == "sqlite":
            return SqliteProvider()
        elif db_type == "mysql":
            return MySqlProvider()
        elif db_type == "pgsql":
            return PgSqlProvider()
