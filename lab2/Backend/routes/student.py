# routes/student.py

from flask import Blueprint, request, jsonify
import sqlite3
from db import get_db_connection, DB_TYPE

bp_student = Blueprint('student', __name__)

@bp_student.route('/request', methods=['POST'])
def create_student_request():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400

    user_id     = data.get('user_id')
    subject     = data.get('subject')
    city        = data.get('city')
    description = data.get('description')
    if not user_id or not subject:
        return jsonify({'success': False, 'message': '用户ID和科目是必填'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()

    # 验证用户存在且角色为 student
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    else:
        cur.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    user_role = row[0] if isinstance(row, tuple) else row['role']
    if user_role != 'student':
        conn.close()
        return jsonify({'success': False, 'message': '只有学生用户可以创建需求信息'}), 403

    # 插入新的学生需求
    if DB_TYPE == 'sqlite':
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
def list_requests():
    subject_filter = request.args.get('subject')
    city_filter    = request.args.get('city')

    conn = get_db_connection()
    cur  = conn.cursor()

    if subject_filter and city_filter:
        if DB_TYPE == 'sqlite':
            query = (
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.subject LIKE ? AND sr.city = ?"
            )
            cur.execute(query, ('%' + subject_filter + '%', city_filter))
        else:
            query = (
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.subject LIKE %s AND sr.city = %s"
            )
            cur.execute(query, ('%' + subject_filter + '%', city_filter))

    elif subject_filter:
        if DB_TYPE == 'sqlite':
            query = (
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.subject LIKE ?"
            )
            cur.execute(query, ('%' + subject_filter + '%',))
        else:
            query = (
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.subject LIKE %s"
            )
            cur.execute(query, ('%' + subject_filter + '%',))

    elif city_filter:
        if DB_TYPE == 'sqlite':
            query = (
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.city = ?"
            )
            cur.execute(query, (city_filter,))
        else:
            query = (
                "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
                "FROM student_request sr JOIN users u ON sr.user_id = u.id "
                "WHERE sr.city = %s"
            )
            cur.execute(query, (city_filter,))

    else:
        query = (
            "SELECT sr.id, sr.subject, sr.city, sr.description, u.id AS user_id, u.name "
            "FROM student_request sr JOIN users u ON sr.user_id = u.id"
        )
        cur.execute(query)

    rows = cur.fetchall()
    conn.close()

    requests_list = []
    for row in rows:
        if isinstance(row, sqlite3.Row):
            requests_list.append(dict(row))
        else:
            requests_list.append({
                'id':          row[0],
                'subject':     row[1],
                'city':        row[2],
                'description': row[3],
                'user_id':     row[4],
                'name':        row[5]
            })

    return jsonify({'success': True, 'requests': requests_list})