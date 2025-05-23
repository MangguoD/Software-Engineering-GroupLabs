# routes/__init__.py

"""
Routes 包的初始化模块，导入并暴露各子模块的 Blueprint 供 app.py 注册使用。
"""

from .auth import bp_auth
from .tutor import bp_tutor
from .student import bp_student
from .recommend import bp_recommend
from .review import bp_review
from .qa import bp_qa

__all__ = [
    'bp_auth',
    'bp_tutor',
    'bp_student',
    'bp_recommend',
    'bp_review',
    'bp_qa',
]