# app.py - Flask 后端主程序
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
try:
    import pymysql
except ImportError:
    pymysql = None

# 数据库配置
DB_TYPE = 'sqlite'  # 使用'sqlite'或'mysql'
DB_NAME = '../database/tutoring.db'  # SQLite数据库文件路径 或 MySQL数据库名
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'

app = Flask(__name__)
CORS(app)  # 允许跨域请求，便于前端开发调试

# 获取数据库连接的辅助函数
def get_db_connection():
    if DB_TYPE == 'sqlite':
        # 连接SQLite数据库文件
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        # 查询结果作为字典返回
        conn.row_factory = sqlite3.Row
        return conn
    elif DB_TYPE == 'mysql':
        if pymysql is None:
            raise Exception('未安装pymysql驱动。如使用MySQL，请安装PyMySQL库。')
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8mb4')
        return conn
    else:
        raise Exception('不支持的 DB_TYPE 类型')

# 用户注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')
    if not username or not password or not name or not role:
        return jsonify({'success': False, 'message': '用户名、密码、姓名和角色均为必填'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    # 检查用户名是否已存在
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM users WHERE username=?", (username,))
    else:
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    exists = cur.fetchone()
    if exists:
        conn.close()
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    # 插入新用户
    if DB_TYPE == 'sqlite':
        cur.execute("INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)",
                    (username, password, role, name))
    else:
        cur.execute("INSERT INTO users (username, password, role, name) VALUES (%s, %s, %s, %s)",
                    (username, password, role, name))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '注册成功，请登录'})

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT id, role, name FROM users WHERE username=? AND password=?", (username, password))
    else:
        cur.execute("SELECT id, role, name FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        # 取出用户信息
        user_id = user[0] if isinstance(user, tuple) or isinstance(user, list) else user['id']
        role = user[1] if isinstance(user, tuple) or isinstance(user, list) else user['role']
        name = user[2] if isinstance(user, tuple) or isinstance(user, list) else user['name']
        return jsonify({'success': True, 'user': {'id': user_id, 'role': role, 'name': name}})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

# 发布家教信息（家教用户创建个人辅导资料）
@app.route('/tutor/profile', methods=['POST'])
def create_tutor_profile():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400
    user_id = data.get('user_id')
    subjects = data.get('subjects')
    city = data.get('city')
    description = data.get('description')
    if not user_id or not subjects:
        return jsonify({'success': False, 'message': '用户ID和科目是必填'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    # 验证用户存在且角色为tutor
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT role FROM users WHERE id=?", (user_id,))
    else:
        cur.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    user_role = row[0] if isinstance(row, tuple) or isinstance(row, list) else row['role']
    if user_role != 'tutor':
        conn.close()
        return jsonify({'success': False, 'message': '只有家教用户可以创建家教信息'}), 403
    # 检查是否已存在该用户的家教信息
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM tutor_profile WHERE user_id=?", (user_id,))
    else:
        cur.execute("SELECT id FROM tutor_profile WHERE user_id=%s", (user_id,))
    exists = cur.fetchone()
    if exists:
        conn.close()
        return jsonify({'success': False, 'message': '家教信息已存在，请勿重复创建'}), 400
    # 插入新的家教信息
    if DB_TYPE == 'sqlite':
        cur.execute("INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (?, ?, ?, ?)",
                    (user_id, subjects, city, description))
    else:
        cur.execute("INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (%s, %s, %s, %s)",
                    (user_id, subjects, city, description))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '家教信息创建成功'})

# 发布学生辅导需求（学生用户发布求辅导信息）
@app.route('/student/request', methods=['POST'])
def create_student_request():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400
    user_id = data.get('user_id')
    subject = data.get('subject')
    city = data.get('city')
    description = data.get('description')
    if not user_id or not subject:
        return jsonify({'success': False, 'message': '用户ID和科目是必填'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    # 验证用户存在且角色为student
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT role FROM users WHERE id=?", (user_id,))
    else:
        cur.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    user_role = row[0] if isinstance(row, tuple) or isinstance(row, list) else row['role']
    if user_role != 'student':
        conn.close()
        return jsonify({'success': False, 'message': '只有学生用户可以创建需求信息'}), 403
    # 插入新的学生需求
    if DB_TYPE == 'sqlite':
        cur.execute("INSERT INTO student_request (user_id, subject, city, description) VALUES (?, ?, ?, ?)",
                    (user_id, subject, city, description))
    else:
        cur.execute("INSERT INTO student_request (user_id, subject, city, description) VALUES (%s, %s, %s, %s)",
                    (user_id, subject, city, description))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '需求发布成功'})

# 获取家教列表（可选按科目/城市过滤）
@app.route('/tutors', methods=['GET'])
def list_tutors():
    subject_filter = request.args.get('subject')
    city_filter = request.args.get('city')
    conn = get_db_connection()
    cur = conn.cursor()
    if subject_filter and city_filter:
        if DB_TYPE == 'sqlite':
            query = "SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                    "WHERE tutor_profile.subjects LIKE ? AND tutor_profile.city = ?"
            cur.execute(query, ('%' + subject_filter + '%', city_filter))
        else:
            query = "SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                    "WHERE tutor_profile.subjects LIKE %s AND tutor_profile.city = %s"
            cur.execute(query, ('%' + subject_filter + '%', city_filter))
    elif subject_filter:
        if DB_TYPE == 'sqlite':
            query = "SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                    "WHERE tutor_profile.subjects LIKE ?"
            cur.execute(query, ('%' + subject_filter + '%',))
        else:
            query = "SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                    "WHERE tutor_profile.subjects LIKE %s"
            cur.execute(query, ('%' + subject_filter + '%',))
    elif city_filter:
        if DB_TYPE == 'sqlite':
            query = "SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                    "WHERE tutor_profile.city = ?"
            cur.execute(query, (city_filter,))
        else:
            query = "SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                    "WHERE tutor_profile.city = %s"
            cur.execute(query, (city_filter,))
    else:
        query = "SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id"
        cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    # 格式化查询结果为列表
    tutors_list = []
    for row in rows:
        if isinstance(row, sqlite3.Row):
            tutor = dict(row)
        else:
            tutor = {
                'id': row[0],
                'subjects': row[1],
                'city': row[2],
                'description': row[3],
                'user_id': row[4],
                'name': row[5]
            }
        tutors_list.append(tutor)
    return jsonify({'success': True, 'tutors': tutors_list})

# 获取学生需求列表（可选按科目/城市过滤）
@app.route('/requests', methods=['GET'])
def list_requests():
    subject_filter = request.args.get('subject')
    city_filter = request.args.get('city')
    conn = get_db_connection()
    cur = conn.cursor()
    if subject_filter and city_filter:
        if DB_TYPE == 'sqlite':
            query = "SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                    "FROM student_request JOIN users ON student_request.user_id = users.id " \
                    "WHERE student_request.subject LIKE ? AND student_request.city = ?"
            cur.execute(query, ('%' + subject_filter + '%', city_filter))
        else:
            query = "SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                    "FROM student_request JOIN users ON student_request.user_id = users.id " \
                    "WHERE student_request.subject LIKE %s AND student_request.city = %s"
            cur.execute(query, ('%' + subject_filter + '%', city_filter))
    elif subject_filter:
        if DB_TYPE == 'sqlite':
            query = "SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                    "FROM student_request JOIN users ON student_request.user_id = users.id " \
                    "WHERE student_request.subject LIKE ?"
            cur.execute(query, ('%' + subject_filter + '%',))
        else:
            query = "SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                    "FROM student_request JOIN users ON student_request.user_id = users.id " \
                    "WHERE student_request.subject LIKE %s"
            cur.execute(query, ('%' + subject_filter + '%',))
    elif city_filter:
        if DB_TYPE == 'sqlite':
            query = "SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                    "FROM student_request JOIN users ON student_request.user_id = users.id " \
                    "WHERE student_request.city = ?"
            cur.execute(query, (city_filter,))
        else:
            query = "SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                    "FROM student_request JOIN users ON student_request.user_id = users.id " \
                    "WHERE student_request.city = %s"
            cur.execute(query, (city_filter,))
    else:
        query = "SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                "FROM student_request JOIN users ON student_request.user_id = users.id"
        cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    requests_list = []
    for row in rows:
        if isinstance(row, sqlite3.Row):
            req = dict(row)
        else:
            req = {
                'id': row[0],
                'subject': row[1],
                'city': row[2],
                'description': row[3],
                'user_id': row[4],
                'name': row[5]
            }
        requests_list.append(req)
    return jsonify({'success': True, 'requests': requests_list})

# 获取某家教详情（包括评价）
@app.route('/tutor/<int:user_id>', methods=['GET'])
def get_tutor_detail(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # 查询家教基本信息（通过用户ID关联）
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id WHERE users.id = ?", (user_id,))
    else:
        cur.execute("SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.name " \
                    "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id WHERE users.id = %s", (user_id,))
    profile = cur.fetchone()
    if not profile:
        conn.close()
        return jsonify({'success': False, 'message': '未找到该家教信息'}), 404
    if isinstance(profile, sqlite3.Row):
        tutor_info = dict(profile)
    else:
        tutor_info = {
            'id': profile[0],
            'subjects': profile[1],
            'city': profile[2],
            'description': profile[3],
            'name': profile[4]
        }
    tutor_profile_id = tutor_info['id']
    # 查询该家教的所有评价
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT review.rating, review.comment, users.name as student_name " \
                    "FROM review JOIN users ON review.student_id = users.id WHERE review.tutor_id = ?", (tutor_profile_id,))
    else:
        cur.execute("SELECT review.rating, review.comment, users.name as student_name " \
                    "FROM review JOIN users ON review.student_id = users.id WHERE review.tutor_id = %s", (tutor_profile_id,))
    reviews_rows = cur.fetchall()
    conn.close()
    reviews_list = []
    for row in reviews_rows:
        if isinstance(row, sqlite3.Row):
            review = dict(row)
        else:
            review = {
                'rating': row[0],
                'comment': row[1],
                'student_name': row[2]
            }
        reviews_list.append(review)
    # 计算平均评分
    avg_rating = None
    if reviews_list:
        avg_rating = round(sum([r['rating'] for r in reviews_list]) / len(reviews_list), 1)
    tutor_info['reviews'] = reviews_list
    tutor_info['average_rating'] = avg_rating
    return jsonify({'success': True, 'tutor': tutor_info})

# 获取针对某学生的推荐家教列表
@app.route('/recommend/student/<int:student_id>', methods=['GET'])
def recommend_tutors(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # 找到该学生发布的所有需求
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT subject, city FROM student_request WHERE user_id = ?", (student_id,))
    else:
        cur.execute("SELECT subject, city FROM student_request WHERE user_id = %s", (student_id,))
    reqs = cur.fetchall()
    recommended = []
    seen_tutors = set()
    # 针对每个需求匹配家教
    for req in reqs:
        subject = req[0] if isinstance(req, tuple) or isinstance(req, list) else req['subject']
        city = req[1] if isinstance(req, tuple) or isinstance(req, list) else req['city']
        # 查找科目和城市都匹配的家教
        if DB_TYPE == 'sqlite':
            cur.execute("SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                        "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                        "WHERE tutor_profile.city = ? AND tutor_profile.subjects LIKE ?", (city, '%' + subject + '%'))
        else:
            cur.execute("SELECT tutor_profile.id, tutor_profile.subjects, tutor_profile.city, tutor_profile.description, users.id as user_id, users.name " \
                        "FROM tutor_profile JOIN users ON tutor_profile.user_id = users.id " \
                        "WHERE tutor_profile.city = %s AND tutor_profile.subjects LIKE %s", (city, '%' + subject + '%'))
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
                    'name': tutor[5]
                }
            if tid not in seen_tutors:
                seen_tutors.add(tid)
                recommended.append(tutor_data)
    conn.close()
    return jsonify({'success': True, 'recommended_tutors': recommended})

# 获取针对某家教的推荐学生需求列表
@app.route('/recommend/tutor/<int:tutor_user_id>', methods=['GET'])
def recommend_students(tutor_user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # 找到该家教的科目列表和城市
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT subjects, city FROM tutor_profile WHERE user_id = ?", (tutor_user_id,))
    else:
        cur.execute("SELECT subjects, city FROM tutor_profile WHERE user_id = %s", (tutor_user_id,))
    profile = cur.fetchone()
    if not profile:
        conn.close()
        return jsonify({'success': False, 'message': '未找到该家教信息'})
    subjects_str = profile[0] if isinstance(profile, tuple) or isinstance(profile, list) else profile['subjects']
    city = profile[1] if isinstance(profile, tuple) or isinstance(profile, list) else profile['city']
    subjects_list = [s.strip() for s in subjects_str.split(',')] if subjects_str else []
    recommended = []
    seen_reqs = set()
    # 针对家教每个科目匹配学生需求
    for subj in subjects_list:
        if DB_TYPE == 'sqlite':
            cur.execute("SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                        "FROM student_request JOIN users ON student_request.user_id = users.id " \
                        "WHERE student_request.city = ? AND student_request.subject = ?", (city, subj))
        else:
            cur.execute("SELECT student_request.id, student_request.subject, student_request.city, student_request.description, users.id as user_id, users.name " \
                        "FROM student_request JOIN users ON student_request.user_id = users.id " \
                        "WHERE student_request.city = %s AND student_request.subject = %s", (city, subj))
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
                    'name': req[5]
                }
            if rid not in seen_reqs:
                seen_reqs.add(rid)
                recommended.append(req_data)
    conn.close()
    return jsonify({'success': True, 'recommended_requests': recommended})

# 提交评价（学生给家教写评价）
@app.route('/review', methods=['POST'])
def submit_review():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '缺少请求数据'}), 400
    tutor_id = data.get('tutor_id')    # 家教信息ID（tutor_profile.id）
    student_id = data.get('student_id')  # 学生用户ID
    rating = data.get('rating')
    comment = data.get('comment')
    if not tutor_id or not student_id or rating is None:
        return jsonify({'success': False, 'message': '缺少必要的评价信息'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    # 验证家教信息存在
    if DB_TYPE == 'sqlite':
        cur.execute("SELECT id FROM tutor_profile WHERE id = ?", (tutor_id,))
    else:
        cur.execute("SELECT id FROM tutor_profile WHERE id = %s", (tutor_id,))
    tutor_profile_exists = cur.fetchone()
    if not tutor_profile_exists:
        conn.close()
        return jsonify({'success': False, 'message': '家教信息不存在'}), 404
    # 插入评价
    if DB_TYPE == 'sqlite':
        cur.execute("INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (?, ?, ?, ?)",
                    (tutor_id, student_id, rating, comment if comment else ''))
    else:
        cur.execute("INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (%s, %s, %s, %s)",
                    (tutor_id, student_id, rating, comment if comment else ''))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '评价提交成功'})

# 问答接口（简单的规则匹配或NLP应答）
@app.route('/qa', methods=['GET'])
def qa():
    question = request.args.get('question') or ''
    question = question.strip()
    if not question:
        return jsonify({'answer': '请提供问题'}), 400
    q = question
    answer = ''
    if '注册' in q:
        answer = '您可以通过点击注册按钮并填写用户名、密码和角色来注册帐户。'
    elif '登录' in q:
        answer = '请在登录页面输入您的用户名和密码进行登录。'
    elif '发布' in q and '家教' in q:
        answer = '作为家教用户，您可以在登录后前往“发布家教信息”页面填写您的科目、城市和简介以发布家教信息。'
    elif '发布' in q and '需求' in q:
        answer = '作为学生用户，您可以在登录后前往“发布需求”页面填写需要辅导的科目、所在城市和具体要求以发布需求信息。'
    elif '匹配' in q or '推荐' in q:
        answer = '系统会根据科目和城市自动推荐合适的家教或学生。例如，数学科目在北京的学生将推荐北京的数学家教。'
    elif '查询' in q or '搜索' in q:
        answer = '您可以通过“查找家教”或“查找学生”功能按科目或城市搜索列表。'
    elif '评价' in q or '评论' in q:
        answer = '在家教详情页面，学生可以对家教进行评分和评论，以提供反馈。'
    else:
        answer = '抱歉，我目前无法回答您的问题。'
    return jsonify({'question': question, 'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)