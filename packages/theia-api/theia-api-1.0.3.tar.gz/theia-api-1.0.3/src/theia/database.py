
import asyncio
import logging
import functools
from typing import AsyncGenerator, Union, Type, List, AsyncIterator, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncConnection
from sqlalchemy import text, delete, update, select, column, Result, func

from datetime import datetime
from contextlib import asynccontextmanager

from theia.metaclass import SingletonMetaCls
from theia.model import OrmModel


def with_session(method):
    """
    用于装饰CRUD方法, 兼容事务, 方法没有带事务连接则构造
    """
    @functools.wraps(method)
    async def wrapper(db_manager, *args, **kwargs):
        session = kwargs.get("session", None)
        if session:
            return await method(db_manager, *args, **kwargs)
        else:
            async with db_manager.transaction() as session:
                kwargs["session"] = session
                return await method(db_manager, *args, **kwargs)
    return wrapper

class SQLAlchemyManager(metaclass=SingletonMetaCls):

    DB_URL_TPL = "{protocol}://{user}:{password}@{host}:{port}/{db}"

    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 3306,
                 user: str = "",
                 password: str = "",
                 db_name: str = "",
                 pool_size: int = 30,
                 pool_pre_ping: bool = True,
                 pool_recycle: int = 600,
                 log: Union[logging.Logger] = None,
                 **kwargs
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.pool_size = pool_size
        self.pool_pre_ping = pool_pre_ping
        self.pool_recycle = pool_recycle
        self.log = log or logging

        self.db_engine: AsyncEngine = None
        self.session_factory: async_sessionmaker = None

    def get_db_url(self, protocol: str = "mysql+aiomysql"):
        """
        组合数据库连接URI
        """
        db_url = self.DB_URL_TPL.format(protocol=protocol, user=self.user, password=self.password,
                                        host=self.host, port=self.port, db=self.db_name)
        return db_url

    def init_db_engine(self, protocol: str):
        """
        初始化DB引擎
        """
        db_url = self.get_db_url(protocol)
        self.log.info(f"init_db_engine => {db_url}")

        self.db_engine = create_async_engine(url=db_url, pool_size=self.pool_size, pool_recycle=self.pool_recycle,
                                             pool_pre_ping=self.pool_pre_ping, echo=False, echo_pool=False,
                                             max_overflow=5)

        self.session_factory = async_sessionmaker(bind=self.db_engine, autoflush=False,
                                                  autocommit=False, expire_on_commit=False, class_=AsyncSession)

        return self.db_engine


class DBManager(metaclass=SingletonMetaCls):

    DB_CLIENT: SQLAlchemyManager = None
    orm_model: Type[OrmModel] = None

    @classmethod
    def bind_engine(cls, db_client: SQLAlchemyManager):
        """
        绑定DB引擎对象
        """
        cls.DB_CLIENT = db_client
        return cls.DB_CLIENT

    @classmethod
    @asynccontextmanager
    async def transaction(cls) -> AsyncGenerator[AsyncSession, None]:
        """
        事务上下文管理器
        """
        async with cls.DB_CLIENT.session_factory() as session:
            async with session.begin():
                yield session

    @classmethod
    @asynccontextmanager
    async def connection(cls) -> AsyncIterator[AsyncConnection]:
        """
        数据库引擎连接上下文管理器
        """
        async with cls.DB_CLIENT.db_engine.begin() as conn:
            yield conn

    @with_session
    async def bulk_add(self, models: List[Union[OrmModel, dict]], *, orm_model: Type[OrmModel] = None,
                       flush: bool = False, session: AsyncSession = None) -> List[OrmModel]:
        """
        批量插入数据

        参数:
            models      ORM映射类实例对象列表或数据字典列表
            orm_model   ORM表映射类
            flush       刷新对象状态, 默认不刷新
            session     数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            成功插入的对象列表
        """
        orm_model = orm_model or self.orm_model
        for i, m in enumerate(models):
            if isinstance(m, dict):
                models[i] = orm_model(**m)

        session.add_all(models)
        if flush:
            await session.flush(models)
        return models

    @with_session
    async def add(self, model: [OrmModel, dict], *, orm_model: Type[OrmModel] = None,
                  session: AsyncSession = None) -> int:
        """
        插入一条数据

        参数:
            model       ORM映射类实例对象或数据字典
            orm_model   ORM表映射类
            session     数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            返回新增的ID
        """
        orm_model = orm_model or self.orm_model
        if isinstance(model, dict):
            model = orm_model(**model)

        session.add(model)
        await session.flush(objects=[model])
        return model.id

    @with_session
    async def delete(self, *, conds: list = None, orm_model: Type[OrmModel] = None,
                     logic_del: bool = False, logic_field: str = "deletetime", logic_del_set_value: Any = None,
                     session: AsyncSession = None) -> int:
        """
        通用删除

        参数:
            conds               条件列表, e.g. [UserTable.id == 1, UserTable.name == "hi"]
            orm_model           ORM表映射类
            logic_del           逻辑删除, False为物理删除, True为逻辑删除, 默认值为 False
            logic_field         逻辑删除更新字段, 默认为deletetime
            logic_del_set_value 逻辑删除字段设置的值
            session             数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            返回删除的记录数
        """
        orm_model = orm_model or self.orm_model

        if logic_del:
            logic_del_info = dict()
            logic_del_info[logic_field] = logic_del_set_value or datetime.now()
            delete_sql = update(orm_model).where(*conds).values(**logic_del_info)
        else:
            delete_sql = delete(orm_model).where(*conds)

        result = await session.execute(delete_sql)

        return result.rowcount

    @with_session
    async def delete_by_id(self, pk_id: int, *, orm_model: Type[OrmModel] = None,
                           logic_del: bool = False, logic_field: str = "deletetime", logic_del_set_value: Any = None,
                           session: AsyncSession = None) -> int:
        """
        根据主键ID删除

        参数:
            pk_id               主键ID值
            orm_model           ORM表映射类
            logic_del           逻辑删除, False为物理删除, True为逻辑删除, 默认值为 False
            logic_field         逻辑删除更新字段, 默认为deletetime
            logic_del_set_value 逻辑删除字段设置的值
            session             数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            返回删除的记录数
        """
        orm_model = orm_model or self.orm_model
        conds = [orm_model.id == pk_id]
        return await self.delete(conds=conds, orm_model=orm_model, logic_del=logic_del, logic_field=logic_field,
                                 logic_del_set_value=logic_del_set_value, session=session)

    @with_session
    async def bulk_delete_by_ids(self, pk_ids: list, *, orm_model: Type[OrmModel] = None,
                                 logic_del: bool = False, logic_field: str = "deletetime",
                                 logic_del_set_value: Any = None,
                                 session: AsyncSession = None) -> int:
        """
        根据主键ID批量删除

        参数:
            pk_ids              主键ID列表
            orm_model           ORM表映射类
            logic_del           逻辑删除, False为物理删除, True为逻辑删除, 默认值为 False
            logic_field         逻辑删除更新字段, 默认为deletetime
            logic_del_set_value 逻辑删除字段设置的值
            session             数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            返回删除的记录数
        """
        orm_model = orm_model or self.orm_model
        conds = [orm_model.id.in_(pk_ids)]
        return await self.delete(conds=conds, orm_model=orm_model, logic_del=logic_del, logic_field=logic_field,
                                 logic_del_set_value=logic_del_set_value, session=session)

    @with_session
    async def _query(self, *, cols: list = None, orm_model: OrmModel = None, conds: list = None,
                     orders: list = None, limit: int = None, offset: int = 0,
                     session: AsyncSession = None) -> Result[Any]:
        """
        通用查询

        参数:
            cols            查询的数据字段
            orm_model       ORM表映射类
            conds           查询的条件列表
            orders          排序列表, 默认id升序
            limit           限制数量
            offset          数据偏移量
            session         数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            查询的结果集
        """
        cols = cols or []
        cols = [column(cols) if isinstance(x, str) else x for x in cols]
        conditions = conds or []
        orders = orders or [column("id")]
        orm_model = orm_model or self.orm_model

        if cols:
            sql = select(*cols).select_from(orm_model).where(*conditions).order_by(*orders)
        else:
            sql = select(orm_model).where(*conditions).order_by(*orders)

        if limit:
            sql = sql.limit(limit).offset(offset)

        result = await session.execute(sql)

        return result

    @with_session
    async def query_one(self, *, cols: list = None, orm_model: OrmModel = None, conds: list = None,
                        orders: list = None, flat: bool = False,
                        session: AsyncSession = None) -> Union[dict, OrmModel, Any]:
        """
        单行查询

        参数:
            cols            查询的数据字段
            orm_model       ORM表映射类
            conds           查询的条件列表
            orders          排序列表, 默认id升序
            flat            单字段时扁平化处理, 没有列名只有值
            session         数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            查询数据对象或字典
        """
        result = await self._query(cols=cols, orm_model=orm_model, conds=conds, orders=orders, limit=1, session=session)
        if not cols:
            return result.scalar_one()

        if flat and len(cols) == 1:
            return result.scalar_one()

        return result.mappings().one() or {}

    @with_session
    async def query_all(self, *, cols: list = None, orm_model: OrmModel = None, conds: list = None,
                        orders: list = None, flat: bool = False, limit: int = None, offset: int = 0,
                        session: AsyncSession = None) -> Union[List[dict], List[OrmModel], Any]:
        """
        多行查询

        参数:
            cols            查询的数据字段
            orm_model       ORM表映射类
            conds           查询的条件列表
            orders          排序列表, 默认id升序
            limit           限制数量
            offset          数据偏移量
            flat            单字段时扁平化处理, 没有列名, 只有值的列表
            session         数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            查询数据对象或字典
        """
        result = await self._query(cols=cols, orm_model=orm_model, conds=conds, orders=orders,
                                   limit=limit, offset=offset, session=session)
        if not cols:
            return result.scalars().all()

        if flat and len(cols) == 1:
            return result.scalars().all()

        return result.mappings().all() or []

    async def list_page(self, *, cols: list = None, orm_model: OrmModel = None, conds: list = None,
                        orders: list = None, page: int = 1, pagesize: int = 20,
                        session: AsyncSession = None) -> tuple:
        """
        单表通用分页查询

        参数:
            cols            查询的数据字段
            orm_model       ORM表映射类
            conds           查询的条件列表
            orders          排序列表, 默认id升序
            page            指定分页
            pagesize        分页大小
            session         数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            查询总数, 分页数据列表
        """
        limit = pagesize
        offset = (page - 1) * pagesize
        return await asyncio.gather(
            self.query_one(cols=[func.count()], orm_model=orm_model, conds=conds,
                           orders=orders, flat=True, session=session),
            self.query_all(cols=cols, orm_model=orm_model, conds=conds, orders=orders,
                           limit=limit, offset=offset, session=session))

    @with_session
    async def update(self, values: dict, *, orm_model: OrmModel = None,
                     conds: list = None, session: AsyncSession = None) -> int:
        """
        更新数据

        参数:
            values          需要更新字段键值对
            orm_model       ORM表映射类
            conds           更新的条件列表
            session         数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            更新影响行数
        """
        orm_model = orm_model or self.orm_model
        conds = conds or []
        values = values or {}
        if not values:
            return 0
        sql = update(orm_model).where(*conds).values(**values)
        result = await session.execute(sql)
        return result.rowcount

    @with_session
    async def run_sql(self, sql: str, *, params: dict = None, query_one: bool = False,
                      col_name: Union[str, None] = None, session: AsyncSession = None) -> Union[dict, List[dict], Any]:
        """
        执行并提交单条SQL语句

        参数:
            sql         要执行的SQL语句
            params      SQL参数绑定列表
            query_one   参数为真则返回结果集的第一条数据字典
            col_name    返回结果集第一条数据字典中指定列名的数据
            session     数据库会话对象, 如果为None则通过装饰器方法内部开启新的事务
        返回值:
            执行SQL的结果
        """
        sql = text(sql)
        result = await session.execute(sql, params)
        data = None
        if query_one:
            data = dict(result.mappings().one()) or {}
        else:
            data = list(result.mappings().all()) or []

        if col_name not in (None, ''):
            data = data[0] if isinstance(data, list) else data
            return data.get(col_name, None)

        return data


db_client = None


def init_async_db(protocol, **kwargs):
    """
    初始化数据库异步连接池并且设置数据库操作基类引擎对象
    """
    global db_client

    if db_client:
        return db_client

    db_client = SQLAlchemyManager(**kwargs)
    db_client.init_db_engine(protocol)
    DBManager.bind_engine(db_client)

    return db_client


