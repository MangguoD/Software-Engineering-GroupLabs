# routes/review.py

from flask import Blueprint, request, jsonify, current_app
from db import get_db_connection
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

bp_review = Blueprint('review', __name__)

limiter = Limiter(key_func=get_remote_address)

@bp_review.before_app_first_request
def init_extensions():
    limiter.init_app(current_app)

@bp_review.route('/', methods=['POST'])
@limiter.limit("15/minute")
def submit_review():
    data = request.get_json() or {}
    tutor_id   = data.get('tutor_id')
    student_id = data.get('student_id')
    rating     = data.get('rating')
    comment    = data.get('comment', '')
    if tutor_id is None or student_id is None or rating is None:
        return jsonify({'success': False, 'message': '缺少必要的评价信息'}), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    # 验证存在性
    if Config.DB_TYPE=='sqlite':
        cur.execute("SELECT id FROM tutor_profile WHERE id = ?", (tutor_id,))
    else:
        cur.execute("SELECT id FROM tutor_profile WHERE id = %s", (tutor_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': '家教信息不存在'}), 404

    # 插入
    if Config.DB_TYPE=='sqlite':
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