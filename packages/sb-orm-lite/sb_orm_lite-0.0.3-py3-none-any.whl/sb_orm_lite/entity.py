from builder import Builder
from mapped_field import Mapped
from provider import ProviderFactory


def entity(klass=None, table_name=None, no_gen=False, db_type=None, gen_select=True):
    def wrap(klass):

        def escape_string(text: str) -> str:
            return text.replace("\"", "\\\"")

        def build_new_methods():
            if "__entity_built__" not in dir(klass):
                if no_gen:
                    setattr(klass, "__entity_built__", True)
                    return

                if "__init__" in dir(klass):
                    setattr(klass, "__old_init__", klass.__init__)
                else:
                    txt = "def __old_init__(self):\r\n\tpass\r\nsetattr(klass, '__old_init__', __old_init__)"
                    exec(txt)

                provider = ProviderFactory.get_provider_by_name(db_type)
                builder = Builder(provider)

                fields = []

                for k, v in klass.__annotations__.items():
                    if isinstance(v, Mapped):
                        if v.name is None:
                            v.name = k
                        if v.field_name is None:
                            v.field_name = k

                        fields.append(v)

                # select all
                if gen_select:
                    txt = f"__select__ = \"{escape_string(builder.build_select(fields, table_name))}\"\r\n"
                    txt += f"setattr(klass, '__select__', __select__)\r\n"
                    txt += f"__where_id__ = \"{escape_string(builder.build_where_id(fields))}\"\r\n"
                    txt += f"setattr(klass, '__where_id__', __where_id__)"
                    exec(txt)

                txt = f"__create__ = \"{escape_string(provider.build_create_table(fields, table_name))}\"\r\n"
                txt += f"setattr(klass, '__create__', __create__)"
                exec(txt)

                # define_map_row(klass, fields)
                txt = "def map_row(self, row):\r\n"
                for i, field in enumerate([f for f in fields if not f.ignore]):
                    txt += f"\tself.{field.name} = row[{i}]\r\n"
                txt += f"setattr(klass, 'map_row', map_row)"
                exec(txt)

                # define_init(non_auto_fields)
                field_list = [f"{f.name}=None" for f in fields if not f.auto_increment and not f.ignore]
                txt = f"def __init__(self, {', '.join(field_list)}):\r\n"
                for field in fields:
                    if field.auto_increment:
                        txt += f"\tself.{field.name} = None\r\n"
                    elif not field.ignore:
                        txt += f"\tself.{field.name} = {field.name}\r\n"
                txt += f"\tself.__old_init__()\r\n"
                # txt += f"\treturn self\r\n"
                txt += "setattr(klass, '__init__', __init__)"
                exec(txt)

                # define_add(non_auto_fields, fields)
                txt = "def add(self, session):\r\n"

                txt += f"\tsql = \"{escape_string(builder.build_insert(fields, table_name))}\"\r\n"
                params = [f"\"{f.name}\" : self.{f.name}" for f in fields if not f.auto_increment and not f.ignore]
                txt += f"\tparams = {{{', '.join(params)}}}\r\n"
                txt += "\tsession.execute(sql, params)\r\n"
                txt += "setattr(klass, 'add', add)"
                exec(txt)

                # update
                txt = "def update(self, session):\r\n"
                # update stations set latitude = :latitude, where name = :name

                txt += f"\tsql = \"{escape_string(builder.build_update(fields, table_name))}\"\r\n"

                params = [f"{provider.escape_name(f.field_name)}: self.{f.name}" for f in fields if not f.primary_key and not f.ignore]
                params.extend([f"{provider.escape_name(f.field_name)}: self.{f.name}" for f in fields if f.primary_key])
                txt += f"\tparams = {{{', '.join(params)}}}\r\n"
                txt += "\tsession.execute(sql, params)\r\n"
                txt += "setattr(klass, 'update', update)"
                exec(txt)

                # delete
                txt = "def delete(self, session):\r\n"
                # delete from stations where name = :name", id)

                id_list = [f"{provider.escape_name(f.field_name)} = {provider.escape_parameter(f.name)}" for f in fields if f.primary_key]

                query = escape_string(f"delete from {provider.escape_name(table_name)} where {' and '.join(id_list)}")
                txt += f"\tsql = \"{query}\"\r\n"

                params = [f"{provider.escape_name(f.field_name)}: self.{f.name}" for f in fields if f.primary_key]
                txt += f"\tparams = {{{', '.join(params)}}}\r\n"
                txt += "\tsession.execute(sql, params)\r\n"
                txt += "setattr(klass, 'delete', delete)"
                exec(txt)

                # define_str(fields)
                txt = "def __str__(self):\r\n"
                txt += f"\treturn f'"
                for field in [f for f in fields]:
                    txt += f"{field.name}: {{self.{field.name}}}, "
                txt = txt[:-2] + "'\r\n"
                txt += f"setattr(klass, '__str__', __str__)"
                exec(txt)

                setattr(klass, "__entity_built__", True)

        build_new_methods()
        return klass

    if klass is None:
        return wrap
    return wrap(klass)
