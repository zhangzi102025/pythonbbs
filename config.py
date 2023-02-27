import os
from datetime import timedelta


class BaseConfig:
    SECRET_KEY = '0123456789'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # session过期时间
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # 设置上传文件的保存路径
    UPLOAD_IMAGE_PATH = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(UPLOAD_IMAGE_PATH):
        os.makedirs(UPLOAD_IMAGE_PATH)
    # 设置数据分页
    PER_PAGE_COUNT = 10


# 开发环境配置
class DevelopmentConfig(BaseConfig):
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/driver_test?charset=utf8mb4"

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "szvsxvawsg@qq.com"
    MAIL_PASSWORD = "bkclqnypqmssddih"
    MAIL_DEFAULT_SENDER = "szvsxvawsg@qq.com"

    # Redis配置
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = '123456'

    # Celery配置
    # 格式 redis://:password@hostname:port/db_number
    CELERY_BROKER_URL = 'redis://:123456@127.0.0.1:6379/1'
    CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379/1'


# 测试环境配置
class TesingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/driver_test?charset=utf8mb4"


# 生产环境配置
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/driver_test?charset=utf8mb4"
