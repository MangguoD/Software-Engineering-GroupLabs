# routes/tutor.py

from flask import Blueprint, request, jsonify, current_app
import sqlite3
from db import get_db_connection
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

bp_tutor = Blueprint('tutor', __name__)

limiter = Limiter(key_func=get_remote_address)
cache   = Cache()

@bp_tutor.before_app_first_request
def init_extensions():
    limiter.init_app(current_app)
    cache.init_app(current_app)

@bp_tutor.route('/profile', methods=['POST'])
@limiter.limit("10/minute")
def create_tutor_profile():
    data = request.get_json() or {}
    user_id    = data.get('user_id')
    subjects   = data.get('subjects')
    city       = data.get('city')
    description= data.get('description')
    if not user_id or not subjects:
        return jsonify({'success': False, 'message': '用户ID和科目是必填'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()

    # 验证用户角色
    if Config.DB_TYPE == 'sqlite':
        cur.execute("SELECT role FROM users WHERE id=?", (user_id,))
    else:
        cur.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    role = row[0] if not hasattr(row, 'keys') else row['role']
    if role != 'tutor':
        conn.close()
        return jsonify({'success': False, 'message': '只有家教用户可以创建家教信息'}), 403

    # 检查重复
    if Config.DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM tutor_profile WHERE user_id=?", (user_id,))
    else:
        cur.execute("SELECT id FROM tutor_profile WHERE user_id=%s", (user_id,))
    if cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '家教信息已存在'}), 400

    # 插入
    if Config.DB_TYPE == 'sqlite':
        cur.execute(
            "INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (?, ?, ?, ?)",
            (user_id, subjects, city, description)
        )
    else:
        cur.execute(
            "INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (%s, %s, %s, %s)",
            (user_id, subjects, city, description)
        )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '家教信息创建成功'})


@bp_tutor.route('/', methods=['GET'])
@limiter.limit("30/minute")
@cache.cached(timeout=Config.CACHE_DEFAULT_TIMEOUT, query_string=True)
def list_tutors():
    subject_filter = request.args.get('subject')
    city_filter    = request.args.get('city')

    conn = get_db_connection()
    cur  = conn.cursor()

    # 构建带筛选的查询，同原逻辑
    if subject_filter and city_filter:
        clause = "tp.subjects LIKE ? AND tp.city = ?" if Config.DB_TYPE=='sqlite' \
                 else "tp.subjects LIKE %s AND tp.city = %s"
        params = ('%'+subject_filter+'%', city_filter)
    elif subject_filter:
        clause = "tp.subjects LIKE ?" if Config.DB_TYPE=='sqlite' else "tp.subjects LIKE %s"
        params = ('%'+subject_filter+'%',)
    elif city_filter:
        clause = "tp.city = ?" if Config.DB_TYPE=='sqlite' else "tp.city = %s"
        params = (city_filter,)
    else:
        clause = None
        params = ()

    base = (
        "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
        "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id"
    )
    if clause:
        base += " WHERE " + clause

    cur.execute(base, params)
    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        if hasattr(r, 'keys'):
            result.append(dict(r))
        else:
            result.append({
                'id':          r[0],
                'subjects':    r[1],
                'city':        r[2],
                'description': r[3],
                'user_id':     r[4],
                'name':        r[5]
            })
    return jsonify({'success': True, 'tutors': result})


@bp_tutor.route('/<int:user_id>', methods=['GET'])
@limiter.limit("30/minute")
@cache.cached(timeout=Config.CACHE_DEFAULT_TIMEOUT)
def get_tutor_detail(user_id):
    conn = get_db_connection()
    cur  = conn.cursor()

    # 查询家教信息
    if Config.DB_TYPE=='sqlite':
        cur.execute(
            "SELECT tp.id, tp.subjects, tp.city, tp.description, u.name "
            "FROM tutor_profile tp JOIN users u ON tp.user_id=u.id WHERE u.id=?",
            (user_id,)
        )
    else:
        cur.execute(
            "SELECT tp.id, tp.subjects, tp.city, tp.description, u.name "
            "FROM tutor_profile tp JOIN users u ON tp.user_id=u.id WHERE u.id=%s",
            (user_id,)
        )
    profile = cur.fetchone()
    if not profile:
        conn.close()
        return jsonify({'success': False, 'message': '未找到该家教信息'}), 404
    info = dict(profile) if hasattr(profile,'keys') else {
        'id': profile[0],
        'subjects': profile[1],
        'city': profile[2],
        'description': profile[3],
        'name': profile[4]
    }
    tutor_profile_id = info['id']

    # 查询评价
    if Config.DB_TYPE=='sqlite':
        cur.execute(
            "SELECT r.rating, r.comment, u.name AS student_name "
            "FROM review r JOIN users u ON r.student_id=u.id WHERE r.tutor_id=?",
            (tutor_profile_id,)
        )
    else:
        cur.execute(
            "SELECT r.rating, r.comment, u.name AS student_name "
            "FROM review r JOIN users u ON r.student_id=u.id WHERE r.tutor_id=%s",
            (tutor_profile_id,)
        )
    reviews = cur.fetchall()
    conn.close()

    lst = []
    for rv in reviews:
        lst.append(dict(rv) if hasattr(rv,'keys') else {
            'rating': rv[0], 'comment': rv[1], 'student_name': rv[2]
        })
    avg = round(sum(r['rating'] for r in lst)/len(lst),1) if lst else None
    info['reviews'] = lst
    info['average_rating'] = avg
    return jsonify({'success': True, 'tutor': info})