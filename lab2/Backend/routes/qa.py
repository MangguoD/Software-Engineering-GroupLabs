# routes/qa.py

from flask import Blueprint, request, jsonify

bp_qa = Blueprint('qa', __name__)

@bp_qa.route('/', methods=['GET'])
def qa():
    """
    问答接口（简单规则匹配）：
    请求参数：?question=<用户提问>
    返回 JSON：
      成功：{"question": "<原问题>", "answer": "<返回回答>"}
      失败：{"answer": "<错误提示>"}，HTTP 400
    """
    question = request.args.get('question', '').strip()
    if not question:
        return jsonify({'answer': '请提供问题'}), 400

    q = question
    # 简单关键词规则匹配
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