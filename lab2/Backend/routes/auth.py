# routes/auth.py

from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TYPE

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400

    username = data.get('username')
    password = data.get('password')
    name     = data.get('name')
    role     = data.get('role')
    if not username or not password or not name or not role:
        return jsonify({'success': False, 'message': '用户名、密码、姓名和角色均为必填'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()

    # 检查用户名是否已存在
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    else:
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '用户名已存在'}), 400

    # 插入新用户
    if DB_TYPE == 'sqlite':
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
def login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()

    # 查询用户
    if DB_TYPE == 'sqlite':
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
    if isinstance(user, dict) or hasattr(user, 'keys'):
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