
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from .apps.base import router as base_router
from .log import log_init
from .cache import get_rds_obj, get_async_rds_obj, AsyncRedis
from .database import init_async_db, SQLAlchemyManager
from .exceptions import TheiaException
import traceback
import os


class Application(FastAPI):

    config: BaseSettings = None

    def __init__(self, config: BaseSettings):

        Application.config = config

        FastAPI.__init__(self, title=config.api_title, version=config.api_version, description=config.api_description,
                         openapi_url=config.prefix + "/openapi.json", docs_url=None, redoc_url=None)

        #  日志配置初始化
        self.log = log_init(config)

        #  挂载静态资源目录
        self.mount(config.base_url + "/public", StaticFiles(directory="public"), name="public")

        if config.cors_enable:
            #  注册后台允许跨域中间件
            self.add_middleware(CORSMiddleware, allow_origins=config.cors_origins,
                                allow_credentials=config.cors_credentials,
                                allow_methods=config.cors_methods, allow_headers=config.cors_headers)

        #  注册应用启动回调
        self.add_event_handler("startup", self.startup)

        #  注册应用关闭回调
        self.add_event_handler("shutdown", self.shutdown)

        #  加载框架基础路由
        self.include_router(base_router)

        #  加载框架模块路由
        for m in config.allow_mod_list:
            if m in config.deny_mod_list:
                continue
            self.load_mod_router(m)

        #  注册全局异常处理
        self.add_exception_handler(RequestValidationError, Application.validation_exception_handler)
        self.add_exception_handler(StarletteHTTPException, Application.global_exception_handler)
        self.add_exception_handler(Exception, Application.global_exception_handler)

    @classmethod
    def bind_config(cls, db_client: SQLAlchemyManager):
        """
        绑定DB引擎对象
        """
        cls.DB_CLIENT = db_client
        return cls.DB_CLIENT

    async def get_aio_redis(self) -> AsyncRedis:
        """
        返回Redis异步连接对象
        """
        return await get_async_rds_obj(**self.config.redis_todict)

    async def startup(self):
        """
        应用启动事件回调
        """
        self.log.info("Application StartUp!!")
        #  worship()

        #  初始化Redis同步连接对象
        #  self.rds = get_rds_obj(**config.redis_todict)

        #  初始化Redis异步连接对象
        self.rds = await self.get_aio_redis()

        #  print(config.mysql_touri)

        #  初始化MySQL异步连接池
        init_async_db(self.config.db_protocol, **self.config.db_todict)

    async def shutdown(self):
        """
        应用关闭事件回调
        """
        self.log.info("Application ShutDown!!")
        await self.rds.close()

    def load_mod_router(self, modname: str) -> None:
        """
        加载应用模块自定义路由
        """
        try:
            #  解析模块路径
            m = modname.split(".")
            if len(m) > 1:
                modroot = m[0]
                modname = m[1]
            else:
                modroot = "apps"
                modname = m[0]

            #  判断模块是否在拒绝模块列表
            if "%s.%s" % (modroot, modname) in self.config.deny_mod_list:
                return

            #  判断是否模块目录批量匹配
            if modname == "*":
                for m in os.listdir(modroot):
                    if m in ["__pycache__", "base"] or m.endswith(".py"):
                        continue
                    if not (os.path.exists("%s/%s/__init__.py" % (modroot, m))
                                or os.path.exists("%s/%s/routers.py" % (modroot, m))):
                        continue

                    self.load_mod_router("%s.%s" % (modroot, m))
                return

            m = __import__("%s.%s" % (modroot, modname))
            self.log.info("__import__: %s" % m)
            m = getattr(m, modname, None)
            self.log.info("getattr module: %s" % m)
            m = getattr(m, "router", None)
            self.log.info("getattr object: %s" % m)
            self.include_router(m)
        except Exception as e:
            self.log.error("%s: %s" % (modname, e))

    @staticmethod
    async def validation_exception_handler(request: Request, e: RequestValidationError) -> JSONResponse:
        """
        请求参数错误处理回调函数
        """
        content = {}
        content["code"] = Application.config.errcode.PARAM.code
        content["data"] = e.args[0]
        content["message"] = Application.config.errcode.PARAM.msg
        return JSONResponse(status_code=content["code"], content=content)

    @staticmethod
    async def global_exception_handler(request: Request, e: Exception) -> JSONResponse:
        content = {}
        content["code"] = Application.config.errcode.SYSTEM.code
        content["data"] = None
        content["message"] = Application.config.errcode.SYSTEM.msg

        if Application.config.debug:
            headers = {k: v for k, v in request.headers.items()}
            if str(e):
                content["message"] = content["message"] + (": %s" % str(e))
            content["url"] = f"{request.url}"
            content["headers"] = f"{headers}"
            content["trace"] = f"{traceback.format_exc()}"

        if isinstance(e, TheiaException):
            theia_content = {"code": e.code, "data": e.detail, "message": e.message}
            if e.is_trace:
                content.update(theia_content)
                theia_content = content
            return JSONResponse(status_code=e.status_code, content=theia_content)

        if isinstance(e, StarletteHTTPException):
            content = {"code": e.status_code, "data": e.detail, "message": e.detail}
            if isinstance(e.detail, str):
                content["data"] = None
            else:
                content["message"] = Application.config.errcode.get_code_msg(e.status_code)
            return JSONResponse(status_code=e.status_code, content=content)

        return JSONResponse(status_code=content["code"], content=content)

