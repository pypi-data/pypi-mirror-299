import datetime

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
    event,
)
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.sql.elements import BinaryExpression

from .utils import get_schema
from ..main import AlphaClass
from ...libs import date_lib
from ..main import AlphaException


def repr(instance):
    columns_values = {}
    if hasattr(instance, "columns"):
        columns_values = {
            x: instance.__dict__[x] if x in instance.__dict__ else None
            for x, y in instance.columns.items()
            if y["show"]
        }
    elif hasattr(instance, "__table__") and hasattr(instance.__table__, "columns"):
        # TODO: update visible
        columns_values = {
            x: instance.__dict__[x] if x in instance.__dict__ else None
            for x, y in instance.__table__.columns.items()
        }
    text = ", ".join("%s=%s" % (x, y) for x, y in columns_values.items())
    return "<%s %r>" % (instance.__tablename__.capitalize(), text)


class AlphaColumn(Column):
    visible = True
    var_name = None

    def __init__(self, *args, visible: bool = True, **kwargs):
        self.visible = visible
        super().__init__(*args, **kwargs)

    def to_json(self):
        key = self.name if not hasattr(self, "_proxy_key") else self._proxy_key
        primary_key, type_ = False, "Text"
        if hasattr(self, "expression"):
            primary_key = getattr(self.expression, "primary_key", primary_key)
            type_ = getattr(self.expression, "type", type_)
        return {
            "name": self.name,
            "key": key,
            "primary_key": primary_key,
            "visible": self.visible,
            "type": type_,
        }


class AlphaTable(AlphaClass):
    # def __new__(class_, *args, **kwargs):
    #    return object.__new__(class_, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.ensure = False

        super().__init__(*args, **kwargs)

    """@declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    def get_table_name(self):
        return self.__name__.lower()"""

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return repr(self)

    def to_json(
        self, relationship: bool = True, disabled_relationships: list[str] = None
    ):
        class_obj = self.__class__
        results_json = {}

        # if it is an AlphaTable
        if hasattr(class_obj, "schema"):
            schema = class_obj.get_schema(
                relationship=relationship, disabled_relationships=disabled_relationships
            )
        else:
            # self.log.error("Missing schema for model <%s>" % str(self.__name__))
            schema = get_schema(
                class_obj,
                relationship=relationship,
                disabled_relationships=disabled_relationships,
            )

        results_json = schema().dump(self)
        return results_json

    def init(self, kwargs: dict, not_none: bool = False):
        kwargs = {
            (x if type(x) == str else x.key): y
            for x, y in kwargs.items()
            if not not_none or (y is not None)
        }
        return self.__init__(**kwargs)

    @classmethod
    def init_from_model(class_obj, model):
        columns = class_obj.get_columns()
        kwargs = {x: y for x, y in model.__dict__.items() if x in columns}
        return class_obj(**kwargs)

    @classmethod
    def instantiate(class_obj, *args, **kwargs):
        """if type(values) == dict:
            return class_obj().init(**values)
        if values
        elif type(values) == list:
            columns ="""
        columns = class_obj.get_columns()
        columns = [x for x in columns if x not in kwargs]
        if len(columns) != len(args):
            raise AlphaException(
                f"args length {len(args)} is incorrect, it must be {len(columns)}"
            )
        for i, column in enumerate(columns):
            kwargs[column] = args[i]
        return class_obj(**kwargs)

    @classmethod
    def get_schema(
        class_obj,
        relationship: bool = True,
        disabled_relationships: list[str] = None,
    ):
        disabled_relationships = disabled_relationships or []
        """if (
            hasattr(class_obj, "schema")
            and class_obj.schema is not None
            and relationship
        ):
            return class_obj.schema
        elif (
            hasattr(class_obj, "schema_without_relationship")
            and class_obj.schema_without_relationship is not None
            and not relationship
        ):
            return class_obj.schema_without_relationship"""
        schema = get_schema(
            class_obj,
            relationship=relationship,
            disabled_relationships=disabled_relationships,
        )
        return schema

    @staticmethod
    def set_attrib_listener(target, value, old_value, initiator):
        tg = target.__table__.c[initiator.key]
        python_type = tg.type.python_type
        if value is None:
            return None
        if python_type == datetime.datetime and type(value) == str:
            return date_lib.str_to_datetime(value)
        if python_type == datetime.datetime and type(value) == datetime.datetime:
            return value
        try:
            return python_type(value)
        except Exception as ex:
            raise

    @classmethod
    def __declare_last__(class_obj):
        for column in class_obj.__table__.columns.values():
            try:
                event.listen(
                    getattr(class_obj, column.key),
                    "set",
                    class_obj.set_attrib_listener,
                    retval=True,
                )
            except Exception as ex:
                continue  # TODO: modify

    @classmethod
    def get_columns(class_obj) -> list[str]:
        columns_names = []

        for col in class_obj.__table__.columns:
            binary_expression = type(col.expression) is BinaryExpression
            if hasattr(col, "prop"):
                column_property = isinstance(col.prop, ColumnProperty)
            if hasattr(col, "name"):
                columns_names.append(col.name)
        return columns_names

    @classmethod
    def get_table_model_structure(class_obj) -> dict[str, str]:
        columns_names = []
        columns = []

        for col in class_obj.__table__.columns:
            binary_expression = type(col.expression) is BinaryExpression
            if hasattr(col, "prop"):
                column_property = isinstance(col.prop, ColumnProperty)
            if hasattr(col, "name"):
                columns_names.append(col.name)

        class_dict = {x: y for x, y in class_obj.__dict__.items()}
        for key, value in class_dict.items():
            if hasattr(value, "expression"):
                if hasattr(value.expression, "name"):
                    if value.expression.name in columns_names:
                        if hasattr(value, "to_json"):
                            column_model = value.to_json()
                            if not hasattr(value, "_proxy_key"):
                                column_model["key"] = key
                            columns.append(column_model)
                        else:
                            print(f"Cannot convert {value}")
        return columns


class AlphaTablePrimaryId(AlphaTable):
    id = AlphaColumn(Integer, primary_key=True, autoincrement=True)


class AlphaTableId(AlphaTable):
    id = AlphaColumn(Integer, autoincrement=True)


class AlphaTableIdPrimary(AlphaTable):
    id = AlphaColumn(Integer, autoincrement=True, primary_key=True)


class AlphaTableUpdateDate(AlphaTable):
    update_date = AlphaColumn(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class AlphaTablePrimaryIdUpdateDate(AlphaTablePrimaryId):
    update_date = AlphaColumn(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class AlphaTableIdUpdateDate(AlphaTableId):
    update_date = AlphaColumn(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class AlphaTableIdUpdateDateCreationDate(AlphaTableId):
    update_date = AlphaColumn(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    creation_date = AlphaColumn(DateTime, default=datetime.datetime.now)


class AlphaFloat(TypeDecorator):
    impl = String

    def process_literal_param(self, value, dialect):
        return str(float(value)) if value is not None else None

    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect):
        return float(value) if value is not None else None


class AlphaInteger(TypeDecorator):
    impl = Integer

    def process_literal_param(self, value, dialect):
        return str(int(value)) if value is not None else None

    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect):
        return float(int) if value is not None else None


"""
    
# creating class dynamically 
def get_table_model(db):
    models = {}
    
    name = "logs"
    models[name] = type(name.capitalize(), (db.Model, ), { 
        # constructor 
        "__tablename__": name, 
        "__repr__": repr,

        "columns": {
            'id':{"show":False},
            'type':{"show":True},
            'origin':{"show":True},
            'message':{"show":True},
            'stack':{"show":True},
            'date':{"show":True}
        },

        "id": db.Column(db.Integer, primary_key=True),
        "type": db.Column(db.String(30)),
        "origin": db.Column(db.String(30)),
        "message": db.Column(db.Text),
        "stack": db.Column(db.Text),
        "date": db.Column(db.DateTime)
    })

    return models
    """
