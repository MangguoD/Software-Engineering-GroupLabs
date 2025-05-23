# routes/tutor.py

from flask import Blueprint, request, jsonify
import sqlite3
from db import get_db_connection, DB_TYPE

bp_tutor = Blueprint('tutor', __name__)

@bp_tutor.route('/profile', methods=['POST'])
def create_tutor_profile():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400

    user_id    = data.get('user_id')
    subjects   = data.get('subjects')
    city       = data.get('city')
    description= data.get('description')
    if not user_id or not subjects:
        return jsonify({'success': False, 'message': '用户ID和科目是必填'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()

    # 验证用户存在且角色为 tutor
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT role FROM users WHERE id=?", (user_id,))
    else:
        cur.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    user_role = row[0]
    if user_role != 'tutor':
        conn.close()
        return jsonify({'success': False, 'message': '只有家教用户可以创建家教信息'}), 403

    # 检查是否已存在该用户的家教信息
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM tutor_profile WHERE user_id=?", (user_id,))
    else:
        cur.execute("SELECT id FROM tutor_profile WHERE user_id=%s", (user_id,))
    if cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '家教信息已存在，请勿重复创建'}), 400

    # 插入新的家教信息
    if DB_TYPE == 'sqlite':
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
def list_tutors():
    subject_filter = request.args.get('subject')
    city_filter    = request.args.get('city')

    conn = get_db_connection()
    cur  = conn.cursor()

    if subject_filter and city_filter:
        if DB_TYPE == 'sqlite':
            query = (
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.subjects LIKE ? AND tp.city = ?"
            )
            cur.execute(query, ('%' + subject_filter + '%', city_filter))
        else:
            query = (
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.subjects LIKE %s AND tp.city = %s"
            )
            cur.execute(query, ('%' + subject_filter + '%', city_filter))

    elif subject_filter:
        if DB_TYPE == 'sqlite':
            query = (
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.subjects LIKE ?"
            )
            cur.execute(query, ('%' + subject_filter + '%',))
        else:
            query = (
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.subjects LIKE %s"
            )
            cur.execute(query, ('%' + subject_filter + '%',))

    elif city_filter:
        if DB_TYPE == 'sqlite':
            query = (
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.city = ?"
            )
            cur.execute(query, (city_filter,))
        else:
            query = (
                "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
                "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id "
                "WHERE tp.city = %s"
            )
            cur.execute(query, (city_filter,))

    else:
        query = (
            "SELECT tp.id, tp.subjects, tp.city, tp.description, u.id AS user_id, u.name "
            "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id"
        )
        cur.execute(query)

    rows = cur.fetchall()
    conn.close()

    tutors_list = []
    for row in rows:
        if isinstance(row, sqlite3.Row):
            tutors_list.append(dict(row))
        else:
            tutors_list.append({
                'id':          row[0],
                'subjects':    row[1],
                'city':        row[2],
                'description': row[3],
                'user_id':     row[4],
                'name':        row[5]
            })

    return jsonify({'success': True, 'tutors': tutors_list})


@bp_tutor.route('/<int:user_id>', methods=['GET'])
def get_tutor_detail(user_id):
    conn = get_db_connection()
    cur  = conn.cursor()

    # 家教基本信息
    if DB_TYPE == 'sqlite':
        cur.execute(
            "SELECT tp.id, tp.subjects, tp.city, tp.description, u.name "
            "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id WHERE u.id = ?",
            (user_id,)
        )
    else:
        cur.execute(
            "SELECT tp.id, tp.subjects, tp.city, tp.description, u.name "
            "FROM tutor_profile tp JOIN users u ON tp.user_id = u.id WHERE u.id = %s",
            (user_id,)
        )
    profile = cur.fetchone()
    if not profile:
        conn.close()
        return jsonify({'success': False, 'message': '未找到该家教信息'}), 404

    # 组装家教信息
    if isinstance(profile, sqlite3.Row):
        tutor_info = dict(profile)
    else:
        tutor_info = {
            'id':          profile[0],
            'subjects':    profile[1],
            'city':        profile[2],
            'description': profile[3],
            'name':        profile[4]
        }
    tutor_profile_id = tutor_info['id']

    # 查询评价
    if DB_TYPE == 'sqlite':
        cur.execute(
            "SELECT r.rating, r.comment, u.name AS student_name "
            "FROM review r JOIN users u ON r.student_id = u.id WHERE r.tutor_id = ?",
            (tutor_profile_id,)
        )
    else:
        cur.execute(
            "SELECT r.rating, r.comment, u.name AS student_name "
            "FROM review r JOIN users u ON r.student_id = u.id WHERE r.tutor_id = %s",
            (tutor_profile_id,)
        )
    reviews_rows = cur.fetchall()
    conn.close()

    reviews_list = []
    for row in reviews_rows:
        if isinstance(row, sqlite3.Row):
            reviews_list.append(dict(row))
        else:
            reviews_list.append({
                'rating':       row[0],
                'comment':      row[1],
                'student_name': row[2]
            })

    # 计算平均评分
    avg_rating = None
    if reviews_list:
        avg_rating = round(sum(r['rating'] for r in reviews_list) / len(reviews_list), 1)

    tutor_info['reviews']        = reviews_list
    tutor_info['average_rating'] = avg_rating

    return jsonify({'success': True, 'tutor': tutor_info})