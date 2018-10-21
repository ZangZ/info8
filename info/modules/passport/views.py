import random
import re

from flask import abort, jsonify
from flask import current_app
from flask import make_response
from flask import request

from info import constants
from info import redis_store
from info.libs.yuntongxun.sms import CCP
from info.utils.response_code import RET
from . import passport_blu
from info.utils.captcha.captcha import captcha




@passport_blu.route("/sms_code", methods=["POST"])
def send_sms_code():
    """发送短信的逻辑"""
    # 1获取数据
    params_dict = request.json


    mobile = params_dict.get("mobile")
    image_code = params_dict.get("image_code")
    image_code_id = params_dict.get("image_code_id")

    # 2校验数据
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数有误")
    if not re.match("1[35678]\\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")
    # 3从redis中取出真实验证码内容
    try:
        real_image_code = redis_store.get("ImageCodeId" + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    if not real_image_code:
        return jsonify(erron=RET.NODATA, errmsg="图片验证码已过期")
    # 4.与用户的验证码内容进行对比,如果不一致,那么返回验证码输入错误
    if real_image_code.upper() != image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入错误")
    # 5如果一致,生成短信验证码的内容(随机数据)
    # 随机数字,保证数字长度为6位,不足补0
    sms_code_str = "%06d" % random.randint(0, 999999)
    current_app.logger.debug("短信验证码内容是:%s" % sms_code_str)
    # 6发送短信验证码
    result = CCP().send_template_sms(mobile, [sms_code_str, constants.SMS_CODE_REDIS_EXPIRES / 5], "1")
    if result != 0:
        # 代表发送不成功
        return jsonify(errno=RET.THIRDERR, errmsg="发送短信失败")

    # 保存验证码内容到redis
    try:
        redis_store.set("SMS_" + mobile, sms_code_str,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    # 7发送成功的结果
    return jsonify(errno=RET.OK, errmsg="发送短信成功")

@passport_blu.route('/image_code')
def get_image_code():
    """
    生成图片验证码并返回
    1. 取到参数
    2. 判断参数是否有值
    3. 生成图片验证码
    4. 保存图片验证码文字内容到redis
    5. 返回验证码图片
    :return:
    """

    # 1. 取到参数
    # args: 取到url中 ? 后面的参数
    image_code_id = request.args.get("imageCodeId", None)
    # 2. 判断参数是否有值
    if not image_code_id:
        return abort(403)

    # 3. 生成图片验证码
    name, text, image = captcha.generate_captcha()

    # 4. 保存图片验证码文字内容到redis
    try:
        redis_store.set("ImageCodeId_" + image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 5. 返回验证码图片
    response = make_response(image)
    # 设置数据的类型，以便浏览器更加智能识别其是什么类型
    response.headers["Content-Type"] = "image/jpg"
    return response

