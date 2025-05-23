# app.py
from flask import Flask
from flask_cors import CORS

# 导入数据库辅助
from db import init_db

# 导入各个蓝图
from routes.auth import bp_auth
from routes.tutor import bp_tutor
from routes.student import bp_student
from routes.recommend import bp_recommend
from routes.review import bp_review
from routes.qa import bp_qa

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 初始化数据库（可选：在这里调用 init_db()）
    # init_db()

    # 注册各个 Blueprint
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_tutor, url_prefix='/tutor')
    app.register_blueprint(bp_student, url_prefix='/student')
    app.register_blueprint(bp_recommend, url_prefix='/recommend')
    app.register_blueprint(bp_review, url_prefix='/review')
    app.register_blueprint(bp_qa, url_prefix='/qa')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)