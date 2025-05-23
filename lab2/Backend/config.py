# config.py
from decouple import config

class Config:
    DEBUG = config('FLASK_DEBUG', default=True, cast=bool)
    # DB
    DB_TYPE     = config('DB_TYPE', 'sqlite')
    DB_NAME     = config('DB_NAME', '../database/tutoring.db')
    DB_HOST     = config('DB_HOST', 'localhost')
    DB_USER     = config('DB_USER', 'root')
    DB_PASSWORD = config('DB_PASSWORD', 'password')
    # 缓存
    CACHE_TYPE            = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = config('CACHE_TIMEOUT', default=60, cast=int)
    # 限流
    RATELIMIT_DEFAULT     = '100/minute'