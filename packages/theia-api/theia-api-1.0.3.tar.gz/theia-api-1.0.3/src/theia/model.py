
import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.expression import ColumnElement

from utils.time import TimeUtil


class OrmModel(AsyncAttrs, DeclarativeBase):

    __abstract__ = True

    def to_dict(self, alias_dict: dict = None, exclude_none = True) -> dict:
        """
        数据库模型转字典

        参数:
            alias_dict      字段别名字典
            exclude_none    默认排查None值
        返回值:
            返回字典格式数据
        """
        result = {}
        alias_dict = alias_dict or {}
        for c in self.__table__.columns:
            if exclude_none and getattr(self, c.name) is None:
                continue
            result[alias_dict.get(c.name, c.name)] = getattr(self, c.name)
        return result

    @classmethod
    def to_column(cls, name: str):
        """
        通过字符串获取列对象
        """
        return getattr(cls, name, None)

    @classmethod
    def to_orders(cls, order: str, sort: str = "asc"):
        """
        解析组合排序选项
        """
        order = cls.to_column(order)
        if order:
            return [order.desc() if sort == "desc" else order.asc()]
        return []

    @classmethod
    def operator_in_val(cls, val: Any):
        """
        IN / NOT IN 操作符的条件值处理
        """
        #  条件值是列表直接返回
        if isinstance(val, list):
            return val

        #  不是字符串类型作为列表第一个元素返回
        if not isinstance(val, str):
            return [val]

        #  列表字符串转列表对象, 转换成功返回列表, 转换失败作为列表第一个元素返回
        try:
            return json.loads(val)
        except:
            return [val]

    @classmethod
    def operator_between_val(cls, val: Any):
        """
        RANGE / BETWEEN 操作符的条件值处理(时间和数字)
        """
        def __to_float(x):
            try:
                x = str(x)
                #  数字中不会带减号字符, 日期才会带减号字符
                if '-' in x and ':' in x:
                    x = TimeUtil().str_to_timestamp(x)
                return float(x)
            except:
                return 0

        if not isinstance(val, list):
            val = str(val).split(",")

        cleft = __to_float(val[0])
        cright = cleft if len(val) == 1 else __to_float(val[1])

        return cleft, cright

    @classmethod
    def get_operators_cond(cls, col: ColumnElement, ops: str, val: Any):
        """
        SQLAlchemy字段查询类型解析及生成查询条件对象

        参数
            col         查询字段列对象
            ops         查询类型字符串
            val         查询字段值

        返回
            返回指定字段查询条件对象
        """
        ops_dict = {
                "=": "__eq__", "==": "__eq__", "!=": "__ne__",
                "<": "__lt__", "<=": "__le__",
                ">": "__gt__", ">=": "__ge__",
                "in": "in_", "not in": "not_in", "range": "between"
        }
        ops = ops.lower()
        ops = ops_dict.get(ops, ops)

        call = getattr(col, ops, col.__eq__)

        if ops in ["like", "ilike"]:
            val = f"%{val}%"
        elif ops in ["in_", "not_in"]:
            val = cls.operator_in_val(val)
        elif ops == "between":
            return call(*cls.operator_between_val(val))

        return call(val)

    @classmethod
    def to_conds(cls, data: dict, op: dict = {}):
        """
        SQLAlchemy查询条件对象列表组合

        参数
            data        查询字段和值键值对
            op          查询字段查询类型

        返回值
            返回SQLAlchemy查询条件对象列表
        """
        conds = []
        for k, v in data.items():
            col = cls.to_column(k)
            if not col:
                continue
            cond = cls.get_operators_cond(col, op.get(k, "__eq__"), v)
            conds.append(cond)
        return conds

    def __repr__(self):
        return str(self.to_dict())

