# routes/qa.py

from flask import Blueprint, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

bp_qa = Blueprint('qa', __name__)

# Initialize limiter
limiter = Limiter(key_func=get_remote_address)

@bp_qa.before_app_first_request
def init_extensions():
    limiter.init_app(current_app)

@bp_qa.route('/', methods=['GET'])
@limiter.limit("30/minute")
def qa():
    """
    问答接口（简单规则匹配 + 限流）：
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
    elif '修改密码' in q or '重置密码' in q:
        answer = '在个人中心页面点击“修改密码”，按照提示输入旧密码和新密码即可完成更新。'
    elif '忘记密码' in q:
        answer = '若忘记密码，请在登录页点击“忘记密码”，输入注册邮箱，我们会发送密码重置链接。'
    elif '退出' in q or '登出' in q:
        answer = '点击页面右上角的“退出登录”按钮即可安全退出您的账户。'
    elif '个人信息' in q or '资料' in q:
        answer = '在个人中心页面，您可以查看并编辑个人资料，包括头像、昵称、联系方式等。'
    elif '客服' in q or '帮助' in q or '联系' in q:
        answer = '如需人工帮助，请前往“联系客服”页面提交工单，我们的客服会尽快联系您。'
    elif '消息' in q or '通知' in q:
        answer = '您可以在“消息”页面查看系统通知和私信。'
    elif '预约' in q:
        answer = '在“我的预约”页面，您可以提前预约家教课程，系统会在课前提醒您。'
    elif '取消预约' in q:
        answer = '在“我的预约”页面点击对应课程后面的“取消”按钮即可取消预约。'
    elif '支付' in q or '付费' in q or '价格' in q:
        answer = '我们支持微信支付、支付宝和信用卡支付，您可以在结算页选择支付方式并完成付款。'
    elif '优惠' in q or '优惠码' in q or '折扣' in q:
        answer = '在支付页面输入有效优惠码可享受折扣，更多活动请查看“优惠活动”页面。'
    elif '订单' in q or '课程记录' in q:
        answer = '您可以在“我的订单”页面查看已购买课程和学习进度。'
    elif '收藏' in q or '关注' in q:
        answer = '点击课程或家教详情页的“收藏”按钮，可将其加入收藏夹，方便下次查看。'
    elif '积分' in q or '余额' in q:
        answer = '在“我的钱包”页面，您可以查看当前积分、余额，并进行充值或兑换操作。'
    elif '隐私' in q:
        answer = '有关隐私保护，请查看“隐私政策”页面，了解我们如何使用和保护您的个人信息。'
    elif '条款' in q or '协议' in q:
        answer = '请查看“用户协议”页面，了解平台使用规则和服务条款。'
    elif '版本' in q or '升级' in q:
        answer = '您可以在设置页查看当前App版本，新版本发布时会自动弹窗提示升级。'
    elif '帮助文档' in q or 'FAQ' in q or '常见问题' in q:
        answer = '请前往“帮助中心”查看操作指南、常见问题解答以及使用教程。'
    elif '反馈' in q or '投诉' in q:
        answer = '欢迎在“意见反馈”页面提交建议或投诉，我们会及时处理。'
    elif '联系客服' in q:
        answer = '如需人工支持，可在“联系客服”页面提交工单，或拨打客服电话：10086。'
    else:
        answer = '抱歉，我目前无法回答您的问题。'

    # 增加对话提示
    answer += " 如需更多帮助，请继续提问，可以选提问：客服, 帮助, 联系, 消息, 通知, 预约, 取消预约, 支付, 付费, 价格, 优惠, 优惠码, 折扣, 订单, 课程记录, 收藏, 关注, 积分, 余额, 隐私, 条款, 协议, 版本, 升级, 帮助文档, FAQ, 常见问题, 反馈, 投诉, 联系客服。"
    return jsonify({'question': question, 'answer': answer})