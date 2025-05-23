# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import logging

# 新增
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

from config import Config

# 导入蓝图
from routes import bp_auth, bp_tutor, bp_student, bp_recommend, bp_review, bp_qa

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 跨域
    CORS(app)
    # 安全头
    Talisman(app)
    # 日志
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    # 缓存
    cache = Cache(app)
    # 限流
    limiter = Limiter(key_func=get_remote_address, app=app)

    # 健康检查
    @app.route('/healthz')
    def healthz():
        return 'OK', 200

    # 注册蓝图
    app.register_blueprint(bp_auth,      url_prefix='/auth')
    app.register_blueprint(bp_tutor,     url_prefix='/tutor')
    app.register_blueprint(bp_student,   url_prefix='/student')
    app.register_blueprint(bp_recommend, url_prefix='/recommend')
    app.register_blueprint(bp_review,    url_prefix='/review')
    app.register_blueprint(bp_qa,        url_prefix='/qa')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])