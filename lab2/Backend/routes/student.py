# routes/student.py

from flask import Blueprint, request, jsonify, current_app
import sqlite3
from db import get_db_connection
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

bp_student = Blueprint('student', __name__)

limiter = Limiter(key_func=get_remote_address)
cache   = Cache()

@bp_student.before_app_first_request
def init_extensions():
    limiter.init_app(current_app)
    cache.init_app(current_app)

@bp_student.route('/request', methods=['POST'])
@limiter.limit("10/minute")
def create_student_request():
    data = request.get_json() or {}
    user_id     = data.get('user_id')
    subject     = data.get('subject')
    city        = data.get('city')
    description = data.get('description')
    if not user_id or not subject:
        return jsonify({'success': False, 'message': '用户ID和科目是必填'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    # 验证角色
    if Config.DB_TYPE=='sqlite':
        cur.execute("SELECT role FROM users WHERE id=?", (user_id,))
    else:
        cur.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    role = row[0] if not hasattr(row,'keys') else row['role']
    if role != 'student':
        conn.close()
        return jsonify({'success': False, 'message': '只有学生可以发布需求'}), 403

    # 插入
    if Config.DB_TYPE=='sqlite':
        cur.execute(
            "INSERT INTO student_request (user_id, subject, city, description) VALUES (?, ?, ?, ?)",
            (user_id, subject, city, description)
        )
    else:
        cur.execute(
            "INSERT INTO student_request (user_id, subject, city, description) VALUES (%s, %s, %s, %s)",
            (user_id, subject, city, description)
        )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '需求发布成功'})


@bp_student.route('/requests', methods=['GET'])
@limiter.limit("30/minute")
@cache.cached(timeout=Config.CACHE_DEFAULT_TIMEOUT, query_string=True)
def list_requests():
    subject_filter = request.args.get('subject')
    city_filter    = request.args.get('city')

    conn = get_db_connection()
    cur  = conn.cursor()

    # 构造条件
    if subject_filter and city_filter:
        clause = "sr.subject LIKE ? AND sr.city = ?" if Config.DB_TYPE=='sqlite' \
                 else "sr.subject LIKE %s AND sr.city = %s"
        params = ('%'+subject_filter+'%', city_filter)
    elif subject_filter:
        clause = "sr.subject LIKE ?" if Config.DB_TYPE=='sqlite' else "sr.subject LIKE %s"
        params = ('%'+subject_filter+'%',)
    elif city_filter:
        clause = "sr.city = ?" if Config.DB_TYPE=='sqlite' else "sr.city = %s"
        params = (city_filter,)
    else:
        clause = None
        params = ()

    base = (
        "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
        "FROM student_request sr JOIN users u ON sr.user_id = u.id"
    )
    if clause:
        base += " WHERE " + clause

    cur.execute(base, params)
    rows = cur.fetchall()
    conn.close()

    out = []
    for r in rows:
        if hasattr(r,'keys'):
            out.append(dict(r))
        else:
            out.append({
                'id':          r[0],
                'subject':     r[1],
                'city':        r[2],
                'description': r[3],
                'user_id':     r[4],
                'name':        r[5]
            })
    return jsonify({'success': True, 'requests': out})