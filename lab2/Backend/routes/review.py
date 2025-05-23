# routes/review.py

from flask import Blueprint, request, jsonify
import sqlite3
from db import get_db_connection, DB_TYPE

bp_review = Blueprint('review', __name__)

@bp_review.route('/', methods=['POST'])
def submit_review():
    """
    学生给家教写评价：
    请求 JSON 格式：{
        "tutor_id": <家教信息表 tutor_profile.id>,
        "student_id": <学生用户 users.id>,
        "rating": <1-5 的整数>,
        "comment": <可选，文字评价>
    }
    返回 JSON：{"success": True/False, "message": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400

    tutor_id   = data.get('tutor_id')
    student_id = data.get('student_id')
    rating     = data.get('rating')
    comment    = data.get('comment', '')

    # 必填检查
    if tutor_id is None or student_id is None or rating is None:
        return jsonify({'success': False, 'message': '缺少必要的评价信息'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()

    # 验证家教信息存在
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM tutor_profile WHERE id = ?", (tutor_id,))
    else:
        cur.execute("SELECT id FROM tutor_profile WHERE id = %s", (tutor_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '家教信息不存在'}), 404

    # 插入评价记录
    if DB_TYPE == 'sqlite':
        cur.execute(
            "INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (?, ?, ?, ?)",
            (tutor_id, student_id, rating, comment)
        )
    else:
        cur.execute(
            "INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (%s, %s, %s, %s)",
            (tutor_id, student_id, rating, comment)
        )
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': '评价提交成功'})