# routes/recommend.py

from flask import Blueprint, jsonify, current_app
import sqlite3
from db import get_db_connection
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

bp_recommend = Blueprint('recommend', __name__)

# Initialize limiter and cache
limiter = Limiter(key_func=get_remote_address)
cache = Cache()

@bp_recommend.before_app_first_request
def init_extensions():
    limiter.init_app(current_app)
    cache.init_app(current_app)

@bp_recommend.route('/student/<int:student_id>', methods=['GET'])
@limiter.limit("30/minute")
@cache.cached(timeout=Config.CACHE_DEFAULT_TIMEOUT)
def recommend_tutors(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # 获取该学生发布的所有需求
    if Config.DB_TYPE == 'sqlite':
        cur.execute("SELECT subject, city FROM student_request WHERE user_id = ?", (student_id,))
    else:
        cur.execute("SELECT subject, city FROM student_request WHERE user_id = %s", (student_id,))
    reqs = cur.fetchall()

    recommended = []
    seen_tutors = set()

    # 针对每个需求匹配家教
    for req in reqs:
        if isinstance(req, sqlite3.Row):
            subject = req['subject']
            city = req['city']
        else:
            subject, city = req[0], req[1]

        if Config.DB_TYPE == 'sqlite':
            cur.execute(
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.city = ? AND tp.subjects LIKE ?",
                (city, '%' + subject + '%')
            )
        else:
            cur.execute(
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.city = %s AND tp.subjects LIKE %s",
                (city, '%' + subject + '%')
            )
        matches = cur.fetchall()

        for tutor in matches:
            if isinstance(tutor, sqlite3.Row):
                tid = tutor['id']
                tutor_data = dict(tutor)
            else:
                tid = tutor[0]
                tutor_data = {
                    'id': tutor[0],
                    'subjects': tutor[1],
                    'city': tutor[2],
                    'description': tutor[3],
                    'user_id': tutor[4],
                    'name': tutor[5],
                }
            if tid not in seen_tutors:
                seen_tutors.add(tid)
                recommended.append(tutor_data)

    conn.close()
    return jsonify({'success': True, 'recommended_tutors': recommended})

@bp_recommend.route('/tutor/<int:tutor_user_id>', methods=['GET'])
@limiter.limit("30/minute")
@cache.cached(timeout=Config.CACHE_DEFAULT_TIMEOUT)
def recommend_students(tutor_user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # 获取家教的科目列表和城市
    if Config.DB_TYPE == 'sqlite':
        cur.execute("SELECT subjects, city FROM tutor_profile WHERE user_id = ?", (tutor_user_id,))
    else:
        cur.execute("SELECT subjects, city FROM tutor_profile WHERE user_id = %s", (tutor_user_id,))
    profile = cur.fetchone()
    if not profile:
        conn.close()
        return jsonify({'success': False, 'message': '未找到该家教信息'})

    if isinstance(profile, sqlite3.Row):
        subjects_str = profile['subjects']
        city = profile['city']
    else:
        subjects_str, city = profile[0], profile[1]

    subjects_list = [s.strip() for s in subjects_str.split(',')] if subjects_str else []

    recommended = []
    seen_reqs = set()

    # 针对家教每个科目匹配学生需求
    for subj in subjects_list:
        if Config.DB_TYPE == 'sqlite':
            cur.execute(
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.city = ? AND sr.subject = ?",
                (city, subj)
            )
        else:
            cur.execute(
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.city = %s AND sr.subject = %s",
                (city, subj)
            )
        matches = cur.fetchall()

        for req in matches:
            if isinstance(req, sqlite3.Row):
                rid = req['id']
                req_data = dict(req)
            else:
                rid = req[0]
                req_data = {
                    'id': req[0],
                    'subject': req[1],
                    'city': req[2],
                    'description': req[3],
                    'user_id': req[4],
                    'name': req[5],
                }
            if rid not in seen_reqs:
                seen_reqs.add(rid)
                recommended.append(req_data)

    conn.close()
    return jsonify({'success': True, 'recommended_requests': recommended})