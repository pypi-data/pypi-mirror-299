from typing import List

from mapped_field import Mapped
from provider import Provider


class Builder(object):
    provider: Provider

    def __init__(self, provider: Provider):
        self.provider = provider

    def build_select(self, fields: List[Mapped], table_name: str) -> str:
        # generate select list
        select_list = []

        for prop in [f for f in fields if not f.ignore]:
            select_list.append(self.provider.escape_name(prop.field_name))

        result = "SELECT "
        result += ", ".join(select_list)
        result += " FROM " + self.provider.escape_name(table_name)

        return result

    def build_where_id(self, fields: List[Mapped]) -> str:
        result = " WHERE "
        id_fields = [f"{self.provider.escape_name(f.field_name)} = {self.provider.escape_parameter(f.name)}" for f in fields if f.primary_key and not f.ignore]
        result += " AND ".join(id_fields)
        return result

    def build_where(self, fields: List[Mapped]) -> str:
        result = " WHERE "
        id_fields = [f"{self.provider.escape_name(f.field_name)} = {self.provider.escape_parameter(f.name)}" for f in fields]
        result += " AND ".join(id_fields)
        return result

    # def _get_value(self, op: Operation):
    #     if isinstance(op.mapped.field_type, String) or isinstance(op.mapped.field_type, DateTime):
    #         return f"'{op.field_or_value}'"
    #     else:
    #         return op.field_or_value
    #
    # def _build_operation(self, op: Operation) -> str:
    #     result = f"{self.provider.escape_name(op.mapped.name)} {op.operation} {self._get_value(op)}"
    #     return result
    #
    # def _build_function(self, where_clause) -> str:
    #     terms = []
    #     clause = where_clause
    #     if not isinstance(where_clause, Function):
    #         clause = And(where_clause)
    #
    #     for expr in clause.expressions:
    #         if isinstance(expr, Or) or isinstance(expr, And):
    #             terms.append(self._build_function(expr))
    #         elif isinstance(expr, Operation):
    #             terms.append(self._build_operation(expr))
    #         else:
    #             ...
    #     result = "("
    #     if isinstance(clause, And):
    #         result += " AND ".join(terms)
    #     else:
    #         result += " OR ".join(terms)
    #
    #     result += ")"
    #     return result
    #
    def build_update(self, fields: List[Mapped], table_name: str):
        result = f"UPDATE {self.provider.escape_name(table_name)} SET "
        terms = []
        for field in [f for f in fields if not f.auto_increment and not f.primary_key]:
            terms.append(f"{self.provider.escape_name(field.field_name)} = {self.provider.escape_parameter(field.name)}")

        result += ", ".join(terms)
        result += self.build_where_id(fields)

        return result

    def build_insert(self, fields: List[Mapped], table_name: str):
        result = f"INSERT INTO {self.provider.escape_name(table_name)} ("
        field_list = []
        for field in fields:
            if not field.auto_increment and not field.ignore:
                field_list.append(field)

        result += ", ".join([self.provider.escape_name(f.field_name) for f in field_list])
        result += ") VALUES ("
        result += ", ".join([self.provider.escape_parameter(f.name) for f in field_list])
        result += ");"

        return result

    # def build_create(self, fields: List[Mapped], table_name: str):
    #     result = f"CREATE TABLE {self.provider.escape_name(table_name)} ("
    #     field_list = []
    #     for field in fields:
    #         field_def = self.provider.build_create_field(field.field_name, field.field_type, field.optional, field.primary_key, field.auto_increment)
    #         field_list.append(field_def)
    #
    #     result += ", ".join(field_list)
    #     result += ");"
    #     return result

    def _build_delete(self, fields: List[Mapped], table_name: str):
        result = f"DELETE FROM {self.provider.escape_name(table_name)} "
        result += self.build_where_id(fields)
        return result
