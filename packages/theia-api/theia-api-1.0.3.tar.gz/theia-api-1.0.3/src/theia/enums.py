
from enum import Enum


class BaseEnum(Enum):

    def __new__(cls, value, desc = None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.desc = desc
        return obj

    @classmethod
    def get_members(cls, exclude_enums: list = None, only_value: bool = False, only_desc: bool = False) -> list:
        members = list(cls)
        if exclude_enums:
            members = [m for m in members if m not in exclude_enums]

        if only_value:
            return [m.value for m in members]

        if only_desc:
            return [m.desc for m in members]

        return members

    @classmethod
    def get_values(cls, exclude_enums: list = None) -> list:
        return cls.get_members(exclude_enums=exclude_enums, only_value=True)

    @classmethod
    def get_names(cls) -> list:
        return list(cls._member_names_)

    @classmethod
    def get_desc(cls, exclude_enums: list = None) -> list:
        return cls.get_members(exclude_enums=exclude_enums, only_desc=True)

    @classmethod
    def get_value_by_desc(cls, enum_desc: str) -> str:
        return {m.desc: m.value for m in cls.get_members()}.get(enum_desc)


class TimeFormatEnum(BaseEnum):
    """
    时间格式化枚举
    """
    DateTime = "%Y-%m-%d %H:%M:%S"
    DateOnly = "%Y-%m-%d"
    TimeOnly = "%H:%M:%S"

    DateTime_CN = "%Y年%m月%d日 %H时%M分%S秒"
    DateOnly_CN = "%Y年%m月%d日"
    TimeOnly_CN = "%H时%M分%S秒"


class TimeUnitEnum(BaseEnum):
    """
    时间单位枚举
    """
    DAYS = "days"
    HOURS = "hours"
    MINUTES = "minutes"
    SECONDS = "seconds"


class ErrCode(BaseEnum):

    SUCCESS   = (200, "成功")
    AUTH      = (401, "认证错误")
    NOT_FOUND = (404, "未找到资源错误")
    PARAM     = (422, "参数传递错误")
    SYSTEM    = (500, "系统内部错误")

    @classmethod
    def get_code_msg(cls, enum_code: int) -> str:
        """
        通过错误码获取错误信息
        """
        return {m.value: m.desc for m in cls.get_members()}.get(enum_code, "")

    @property
    def code(self):
        """
        获取错误码
        """
        return self.value

    @property
    def msg(self):
        """
        获取错误信息
        """
        return self.desc

