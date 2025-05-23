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

# —— 数据库配置 ——
DB_TYPE = 'sqlite'                  # 使用 'sqlite' 或 'mysql'
DB_NAME = '../database/tutoring.db' # SQLite 数据库文件路径，或 MySQL 数据库名
DB_HOST = 'localhost'               # MySQL 主机
DB_USER = 'root'                    # MySQL 用户名
DB_PASSWORD = 'password'            # MySQL 密码


def get_db_connection():
    """
    根据 DB_TYPE 返回数据库连接：
      - sqlite: 返回 sqlite3.Connection，row_factory 设置为 sqlite3.Row
      - mysql : 返回 pymysql.Connection
    抛出异常：
      - 未安装 pymysql 驱动时使用 mysql
      - DB_TYPE 非法时
    """
    if DB_TYPE == 'sqlite':
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        # 使查询结果可以像 dict 一样通过字段名访问
        conn.row_factory = sqlite3.Row
        return conn

    elif DB_TYPE == 'mysql':
        if pymysql is None:
            raise RuntimeError('MySQL 模式下需要安装 PyMySQL：pip install pymysql')
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        return conn

    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE!r}. 仅支持 'sqlite' 或 'mysql'")