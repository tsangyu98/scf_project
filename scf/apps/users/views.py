import json
import random
import logging
import re
from rest_framework_jwt.settings import api_settings
from django.db import DatabaseError
from django.utils import timezone

from users.models import User

looger=logging.getLogger('django')

from django import http
from django.views import View
from django_redis import get_redis_connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from libs.yuntongxun.sms import CCP
from users.serializer import AdminAuthSerializer, RegisterSerializers


class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """

        #  生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        looger.info(sms_code)
        # print(sms_code)

        #  创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')

        #  保存短信验证码
        # 短信验证码有效期，单位：300秒
        redis_conn.setex('sms_%s' % mobile,
                         300,
                         sms_code)

        #  发送短信验证码
        # 短信模板
        CCP().send_template_sms(mobile,[sms_code, 5], 1)

        #  响应结果
        return http.JsonResponse({'code': 0,
                                  'errmsg': '发送短信成功'})

# POST /meiduo_admin/authorizations/
class AdminAuthorizeView(APIView):
    def post(self, request):
        """
        用户登录:
        1. 获取参数并进行校验
        2. 服务器签发jwt token数据
        3. 返回应答
        """
        # 1. 获取参数并进行校验
        serializer = AdminAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 服务器签发jwt token数据(create)
        serializer.save()

        # 3. 返回应答
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterSerializer(APIView):
    """用户注册"""
    def post(self, request):
        """
        用户注册:
        1. 获取参数并进行校验
        2. 服务器签发jwt token数据
        3. 返回应答
        """
        # 1. 获取参数并进行校验
        serializer = RegisterSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 服务器签发jwt token数据(create)
        user=serializer.save()
        user.last_login = timezone.now()

        user.set_password(user.password)
        user.save()
        # 服务器生成jwt token, 保存当前用户的身份信息


        # 组织payload数据的方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token数据的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 组织payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token
        token = jwt_encode_handler(payload)

        # 给user对象增加属性，保存jwt token的数据
        # user.token = token
        serializer.token=token

        # 3. 返回应答
        return Response(serializer.data, status=status.HTTP_201_CREATED)





