import os
from theia.enums import ErrCode
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import computed_field
from typing import Union


class Settings(BaseSettings):

    #  调试模式
    debug: bool = True


    #  API基地址
    base_url: str = "/api"
    #  API版本号
    api_version: str = "v1"
    #  API文档标题
    api_title: str = "Theia API"
    #  API文档简介
    api_description: str = "Theia-API 接口文档"
    #  API地址前缀
    prefix: str = "%s/%s" % (base_url, api_version)


    #  是否允许跨域
    cors_enable: bool = True
    #  只允许跨域的URL, *代表所有
    cors_origins: list = ["http://localhost:8090", "http://127.0.0.1:8090"]
    #  只允许域的方法, *代表所有方法(get post put)
    cors_methods: list = ["*"]
    #  只允许携带的header, *代表所有
    cors_headers: list = ["*"]
    #  是否支持携带cookie
    cors_credentials: bool = True


    #  安全的随机密钥, 用于JWT令牌签名
    jwt_secret_key: str = "vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$"
    #  JWT令牌签名算法
    jwt_algorithm: str = "HS256"
    #  access token 过期时间: 默认值为一天
    access_token_expire_minutes: int = 1440
    #  refresh token 过期时间, 用于刷新token使用, 默认值为两天
    refresh_token_expire_minutes: int = 1440 * 2
    #  access token 缓存时间, 用于刷新token使用, 30分钟
    access_token_cache_minutes: int = 30
    #  access token 获取url
    access_token_url: str = "%s/auth/token" % prefix


    #  应用根路径
    appspath: str = os.path.dirname(os.path.abspath(__file__))
    #  项目根路径
    rootpath: str = os.path.dirname(appspath)
    #  公共目录路径
    public_url: str = "%s/public" % base_url
    #  资源目录路径
    asserts_url: str = "%s/asserts" % public_url
    #  JavaScript文件路径
    js_url: str = "%s/js" % asserts_url
    #  CSS文件路径
    css_url: str = "%s/css" % asserts_url
    #  图片文件路径
    img_url: str = "%s/img" % asserts_url


    #  绑定IP
    host: str = "0.0.0.0"
    #  监听端口号
    port: int = 8090
    #  修改是否动态加载
    is_reload: bool = True
    #  线程数
    workers: int = 1
    #  是否记录访问日志
    access_log: int = 1

    #  日志级别: DEBUG INFO WARNING ERROR CRITICAL
    log_level: str = "INFO"
    #  日志文件路径
    log_path: str = rootpath + "/logs/{time:YYYY-MM-DD}.log"
    #  日志保留时间
    log_retention: str = "14 days"
    #  日志是否异步写入
    log_async: bool = True


    #  需要加载的应用模块列表
    #  allow_mod_list: list = ["apps.user", "apps.token", "tests.db", "tests.rds", "tests.misc"]
    allow_mod_list: list = ["apps.*", "tests.*"]

    #  拒绝加载的应用模块列表
    #  deny_mod_list: list = ["tests.db"]
    deny_mod_list: list = []


    #  错误码
    errcode: object = ErrCode

    # Redis 配置
    redis_host: str = "redis.srv.com"
    redis_port: int = 6379
    redis_password: Union[str, None] = None
    redis_db: int = 0
    redis_decode_response: bool = True
    redis_pool_max: int = 10
    redis_encoding: str = "utf-8"

    # 返回Redis字典配置
    @computed_field  # type: ignore[misc]
    @property
    def redis_todict(self) -> dict:
        return {
            "host": self.redis_host,
            "port": self.redis_port,
            "password": self.redis_password,
            "db": self.redis_db,
            "max_connections": self.redis_pool_max,
            "decode_responses": self.redis_decode_response,
            "encoding": self.redis_encoding,
        }

    #  MySQL 配置
    db_protocol: str = "mysql+asyncmy"
    db_host: str = "db.srv.com"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "123321"
    db_name: str = "theia"
    db_charset: str = "utf8mb4"
    db_prefix: str = "ex"

    # 返回DB字典配置
    @computed_field  # type: ignore[misc]
    @property
    def db_todict(self) -> dict:
        return {
            "host": self.db_host,
            "port": self.db_port,
            "user": self.db_user,
            "password": self.db_password,
            "db_name": self.db_name,
            "charset": self.db_charset,
            "prefix": self.db_prefix,
        }

    # 返回DB URI配置
    @computed_field  # type: ignore[misc]
    @property
    def db_touri(self) -> str:
        url = "%s://%s:%s@%s:%s/%s?charset=%s"
        url = url % (self.db_protocol, self.db_user, self.db_password,
                     self.db_host, self.db_port,
                     self.db_name, self.db_charset)
        return url


    #  环境变量文件定义
    class Config:

        env_file = ".env"


    def __init__(self, *args, **kwargs):
        BaseSettings.__init__(self, *args, **kwargs)

    def __str__(self):
        s = ""
        for k, v in self.__dict__.items():
            if k.startswith("__") and k.endswith("__"):
                continue
            s = s + "%20s: %s %s\n" % (k, v, type(v))
        return s

    def __repr__(self):
        return self.__str__

@lru_cache
def get_settings() -> Settings:
    return Settings()


