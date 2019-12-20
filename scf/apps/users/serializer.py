import re
from rest_framework_jwt.settings import api_settings
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import serializers
from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):


    """用户登录序列化器类"""
    username = serializers.CharField(label='用户名')
    token = serializers.CharField(label='JWT Token', read_only=True)


    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token', 'mobile')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # 获取username和password
        username = attrs['username']
        # username = attrs['username']
        password = attrs['password']

        # 进行用户名和密码校验
        try:
            user = User.objects.get(username=username)#username=username
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            # 校验密码
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')

            # 给attrs中添加user属性，保存登录用户
            #
            attrs['user'] = user

        return attrs

    def create(self, validated_data):
        # 获取登录用户user
        user = validated_data['user']

        # 设置最新登录时间
        user.last_login = timezone.now()
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
        user.token = token

        return user

class RegisterSerializers(serializers.ModelSerializer):

    """用户注册序列化器类"""
    token=serializers.CharField(label='tocken',required=False)
    sms_code=serializers.CharField(label='验证码',read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token','mobile','sms_code')

        extra_kwargs = {
            'password': {
                'write_only': True
            },

        }

    def validate(self, attrs):
        # 获取username和password
            # 给attrs中添加user属性，保存登录用户
        mobile=attrs.get('mobile')
        sms_code=attrs.pop('sms_code',None)
        if not re.match(r'^1[345789]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式不正确')
        # redis_conn = get_redis_connection('verify_code')
        # sms_code_server=redis_conn.get('sms_%s' % mobile)
        # if sms_code_server.decode() != sms_code:
        #     raise serializers.ValidationError('验证码错误')
        return attrs


