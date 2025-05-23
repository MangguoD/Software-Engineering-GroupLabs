# db.py

"""
数据库连接工具模块。
根据 DB_TYPE 的配置，返回 SQLite 或 MySQL 的连接。
"""

import sqlite3
try:
    import pymysql
except ImportError:
    pymysql = None
from config import Config


def get_db_connection():
    """
    根据 Config.DB_TYPE 返回数据库连接：
      - sqlite: 返回 sqlite3.Connection，row_factory 设置为 sqlite3.Row
      - mysql : 返回 pymysql.Connection
    抛出异常：
      - 未安装 pymysql 驱动时使用 mysql
      - DB_TYPE 非法时
    """
    if Config.DB_TYPE == 'sqlite':
        conn = sqlite3.connect(Config.DB_NAME, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    elif Config.DB_TYPE == 'mysql':
        if pymysql is None:
            raise RuntimeError('MySQL 模式下需要安装 PyMySQL：pip install pymysql')
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset='utf8mb4'
        )
        return conn

    else:
        raise ValueError(f"Unsupported DB_TYPE: {Config.DB_TYPE!r}. 仅支持 'sqlite' 或 'mysql'")