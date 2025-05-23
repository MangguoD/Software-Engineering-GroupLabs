# routes/auth.py

from flask import Blueprint, request, jsonify, current_app
from db import get_db_connection
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from schemas import RegisterSchema, LoginSchema

bp_auth = Blueprint('auth', __name__)

# 限流器（只需 key_func）
limiter = Limiter(key_func=get_remote_address)

@bp_auth.before_app_first_request
def init_extensions():
    limiter.init_app(current_app)

@bp_auth.route('/register', methods=['POST'])
@limiter.limit("5/minute")
def register():
    # 输入校验
    schema = RegisterSchema()
    errors = schema.validate(request.json or {})
    if errors:
        return jsonify({'success': False, 'message': errors}), 400
    data = schema.load(request.json)

    username = data['username']
    password = data['password']
    name     = data['name']
    role     = data['role']

    conn = get_db_connection()
    cur  = conn.cursor()

    # 检查用户名是否已存在
    if Config.DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    else:
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '用户名已存在'}), 400

    # 插入新用户
    if Config.DB_TYPE == 'sqlite':
        cur.execute(
            "INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)",
            (username, password, role, name)
        )
    else:
        cur.execute(
            "INSERT INTO users (username, password, role, name) VALUES (%s, %s, %s, %s)",
            (username, password, role, name)
        )
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': '注册成功，请登录'})


@bp_auth.route('/login', methods=['POST'])
@limiter.limit("10/minute")
def login():
    # 输入校验
    schema = LoginSchema()
    errors = schema.validate(request.json or {})
    if errors:
        return jsonify({'success': False, 'message': errors}), 400
    data = schema.load(request.json)

    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cur  = conn.cursor()

    # 查询用户
    if Config.DB_TYPE == 'sqlite':
        cur.execute(
            "SELECT id, role, name FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
    else:
        cur.execute(
            "SELECT id, role, name FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    # 兼容 sqlite3.Row（dict-like）或 tuple
    if hasattr(user, 'keys'):
        user_id = user['id']
        role    = user['role']
        name    = user['name']
    else:
        user_id, role, name = user

    return jsonify({
        'success': True,
        'user': {
            'id':   user_id,
            'role': role,
            'name': name
        }
    })