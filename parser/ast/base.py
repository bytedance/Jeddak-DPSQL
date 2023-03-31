from collections import MutableSequence
import numpy as np

from parser.ast.visitor.tree_visitor import VisitorOrder


class State:
    def __init__(self):
        self.query = None
        self.hint = None

    def __str__(self):
        pass


class ColumnInfo:
    """
        Store table information obtained from metadata.

    """
    def __init__(self):
        super(ColumnInfo, self).__init__()
        self.name = None
        self.bounded = None
        self.is_key = None
        self.max_fre = None
        self.maxval = None
        self.minval = None
        self.clipping_flag = None
        self.columnValue_type = None  #
        self.table_name = None

    def sensitivity(self):
        if self.columnValue_type in ["int", "float", "float64", "int64", "float32", "int32"]:
            if self.minval is not None and self.maxval is not None:
                sens = max(abs(self.maxval), abs(self.minval))
                if sens == 0:
                    return None
                else:
                    return sens
            else:
                return np.inf  # unbounded
        elif self.columnValue_type == "boolean":
            return 1
        else:
            return None

    def evaluate(self, bindings):
        if self.name.lower() in bindings:
            return bindings[self.name.lower()]
        else:
            return None

    def dbtype(self, converter):
        if hasattr(self, "columnValue_dbtype"):
            return self.columnValue_dbtype
        return self.columnValue_type


class MapExpressionInfo:
    """
        Store table information obtained from metadata

    """
    def __init__(self):
        super(MapExpressionInfo, self).__init__()
        self.name = None
        self.bounded = None
        self.is_key = None
        self.key_dbtype = None
        self.key_metas = None
        self.key_metas_event_name_dict = None
        self.key_type = None
        self.max_fre = None
        self.value_dbtype = None
        self.value_type = None
        self.columnValue_type = None
        self.columnValue_dbtype = None
        self.minval = None
        self.maxval = None
        self.key_meta = None
        self.table_name = None

    def sensitivity(self):
        if self.value_type in ["int", "float", "float64", "int64", "float32", "int32"]:
            if self.minval is not None and self.maxval is not None:
                if self.value_type in ["int", "int64", "int32"]:
                    sens = max(abs(int(self.maxval)), abs(int(self.minval)))
                else:
                    sens = max(abs(float(self.maxval)), abs(float(self.minval)))
                if sens == 0:
                    return None
                else:
                    return sens
            else:
                return np.inf  # unbounded
        elif self.value_type == "boolean":
            return 1
        else:
            return None

    def dbtype(self, converter):
        return self.value_dbtype

    def type(self):
        return self.value_type


class Symbol:
    def __init__(self):
        super(Symbol, self).__init__()
        self.name = None
        self.lower = None
        self.upper = None
        self.sens = None

    def sensitivity(self):
        return self.sens


class Seq(MutableSequence):
    def __init__(self, owner, iterable=()):
        self._list = list(iterable)
        self.owner = owner

    def __getitem__(self, key):
        return self._list.__getitem__(key)

    # trigger change handler
    def __setitem__(self, key, item):
        self._list.__setitem__(key, item)
        item.parent = self.owner

    # trigger change handler
    def __delitem__(self, key):
        self._list.__delitem__(key)

    def __len__(self):
        return self._list.__len__()

    # trigger change handler
    def insert(self, index, item):
        self._list.insert(index, item)
        item.parent = self.owner
        item.indexInParent = index
        # self.owner.children[index] = item

    def sensitivity(self):
        for item in self._list:
            return sensitivity_internal(item)

    def evaluate(self, bindings):
        # need to decide what to do with this
        return self._list[0].evaluate(bindings)

    def dbtype(self, converter):
        return self[0].dbtype(converter)

    def type(self):
        return self._list[0].type()


def sensitivity_internal(item):
    if hasattr(item, "symbol"):
        if type(item.symbol) is not Symbol:
            return item.symbol.sensitivity()
        else:
            return item.sensitivity()
    else:
        return item.sensitivity()


class SqlNode:
    def __init__(self):
        self.parent = None
        self.children = {}
        self.indexInParent = None
        # self.state = None
        # self.attributes = None
        # sqlStatement, blockStatement, or expr
        self.type = None

    def __str__(self):
        return " ".join([str(c) for c in self.children.values() if c is not None])

    def __setitem__(self, key, value):
        pass

    def __setattr__(self, key, value):
        # pass
        if key == "parent":
            pass
        elif key == "symbol":
            pass
        elif isinstance(value, SqlNode):
            self.children[key] = value
            value.parent = self
        object.__setattr__(self, key, value)

    def accept(self, visitor, order=VisitorOrder.FORWARD):
        if visitor is None:
            raise Exception("visitor cannot be none")
        visitor.preVisit(self)
        self.accept0(visitor, order)
        visitor.postVisit(self)

    def accept0(self, visitor, order):
        pass

    def sensitivity(self):
        return None

    def clone(self):
        return self


class SqlStatement(SqlNode):
    def __init__(self):
        super(SqlStatement, self).__init__()


class SqlExpr(SqlNode):
    def __init__(self):
        super(SqlExpr, self).__init__()

    def sensitivity(self):
        return None

    def evaluate(self, bindings):
        raise ValueError("We don't know how to evaluate %s" % str(self))

    def type(self):
        return "unknown"
