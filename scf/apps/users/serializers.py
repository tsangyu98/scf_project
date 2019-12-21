import re

from rest_framework import serializers

from answers.models import Label, Question, Reply
from employment.models import Enterprise
from toutiao.models import Comment, Article
from users.models import User




import re
from rest_framework_jwt.settings import api_settings
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import serializers

from toutiao.models import Article
from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):


    """用户登录序列化器类"""
    username = serializers.CharField(label='用户名')
    token = serializers.CharField(label='JWT Token', read_only=True)


    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token', 'mobile','avatar')

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'avatar':{
                'read_only':True
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
        fields = ('id', 'username', 'password', 'token','mobile','sms_code','avatar')

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'avatar':{
                'read_only':True
            }

        }

    def validate(self, attrs):
        # 获取username和password
            # 给attrs中添加user属性，保存登录用户
        mobile=attrs.get('mobile')
        sms_code=attrs.get('sms_code')
        # if not re.match(r'^1[345789]\d{9}$', mobile):
        #     raise serializers.ValidationError('手机号格式不正确')
        # redis_conn = get_redis_connection('verify_code')
        # sms_code_server=redis_conn.get('sms_%s' % mobile)
        # if sms_code_server.decode() != sms_code:
        #     raise serializers.ValidationError('验证码错误')
        return attrs


class Follows(serializers.ModelSerializer):
    '''关注序列化器'''
    # collected_users_id=serializers.ListField(label='s')
    class Meta:
        model =Article
        fields = ('collected_users',)








##########################





# class UserEnterpisesSerializer(serializers.ModelSerializer):
#     '''enterpises具体序列化器类'''
#     recruits = serializers.PrimaryKeyRelatedField(label='职务', many=True, read_only=True,allow_null=True)
#
#     class Meta:
#         model = Enterprise
#         fields = ('id', 'name', 'labels', 'logo', 'recruits', 'summary')
#
#
# class UserReplySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = '__all__'
#
#
# # class UserNameSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model=User
# #         fields=('nickname')
#
# class UserLaberSeralizer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ('id', 'labels')
#
#
# class UserInfoSerializer(serializers.ModelSerializer):
#     '''用户信息系列化器类'''
#     enterpises = UserEnterpisesSerializer(label='具体职务', many=True,allow_null=True)
#     # label=serializers.StringRelatedField(label='标签',many=True)
#     label = UserLaberSeralizer(label='标签', many=True,allow_null=True)
#     questions = serializers.StringRelatedField(label='我的问题', many=True,allow_null=True)
#     answer_question = UserReplySerializer(label='我的回答', many=True,allow_null=True)
#     username = serializers.StringRelatedField(label='用户名',allow_null=True)
#     # answer_question=replys
#     collected_articles = serializers.StringRelatedField(label='我的收藏', many=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'mobile', 'realname', 'birthday', 'sex', 'avatar', 'website',
#                   'email', 'city', 'address', 'label', 'questions', 'answer_question',
#                   'collected_articles', 'enterpises')
#
#
# class LabelsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Label
#         fields = ('id', 'label_name')
#
#
# class QuestionsSerializer(serializers.ModelSerializer):
#     labels = serializers.StringRelatedField(many=True,allow_null=True)
#     replytime = serializers.CharField(allow_null=True)
#     replyname = serializers.CharField(allow_null=True)
#     class Meta:
#         model = Question
#         fields = ('id', 'createtime', 'labels', 'reply', 'replyname',
#                   'replytime', 'title', 'unuseful_count', 'useful_count',
#                   'user', 'visits')
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'avatar')
#
#
# class SubsSerializer(serializers.ModelSerializer):
#     user = UserSerializer(label='用户', many=True)
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'content', 'createtime', 'useful_count',
#                   'unuseful_count', 'user')
#
#
# class AnswerQuestionSerializer(serializers.ModelSerializer):
#     subs = SubsSerializer(label='用户', many=True,allow_null=True)
#     user = UserSerializer(label='用户', many=True,allow_null=True)
#
#     class Meta:
#         model = Reply
#         fields = ('id', 'content', 'createtime', ' useful_count', 'problem',
#                   'unuseful_count', 'subs', 'user', 'parent')
#
#
# class UserCollectedArticlesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ('id', 'title')
#
#
# class UserCollectedSerializer(serializers.ModelSerializer):
#     articles = UserCollectedArticlesSerializer(label='收藏的文章', many=True,allow_null=True)
#     fans = serializers.PrimaryKeyRelatedField(many=True, read_only=True,allow_null=True)
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'avatar', 'articles', 'fans')
#
#
# class CollectedArticlesSerializer(serializers.ModelSerializer):
#     user = UserCollectedSerializer(label='我的收藏', many=True,allow_null=True)
#     collected_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True,allow_null=True)
#     collected=serializers.SerializerMethodField(allow_null=True)
#     class Meta:
#         model = Article
#         fields = ('id', 'title', 'content', 'createtime', 'user', 'collected_users',
#                   'collected', 'image')
#         def get_collected(self,obj):
#             collected=True
#             return collected
#
# class ContentTypeSerializer(serializers.ModelSerializer):
#     '''接收的信息'''
#     labels = LabelsSerializer(label='标签', many=True,allow_null=True)
#     questions = QuestionsSerializer(label='我的问题', many=True,allow_null=True)
#     answer_question = AnswerQuestionSerializer(label='我的回答', many=True,allow_null=True)
#     collected_articles = CollectedArticlesSerializer(label='我的收藏', many=True,allow_null=True)
#     enterpises = UserEnterpisesSerializer(label='具体职务', many=True,allow_null=True)
#     username = serializers.StringRelatedField(label='用户名')
#
#     class Meta:
#         model = User
#         fields = ('id', 'username',  'mobile', 'realname', 'birthday', 'sex', 'avatar', 'website',
#                   'email', 'city', 'address', 'labels', 'questions', 'answer_question', 'collected_articles',
#                   'enterpises')


# class UserUpdatePasswordSerializer(serializers.ModelSerializer):
#     '''修改密码的序列化器类'''
#
#     class Meta:
#         model=User
#         fields=('password',)
#
#     def update(self,instance,validated_data):
#         instance.set_password(validated_data.get('password'))
#         instance.save()
#         return instance






# 企业信息
class EnterpisesSimpleSerializer(serializers.ModelSerializer):
    recruits = serializers.PrimaryKeyRelatedField(label='招聘需求', queryset=Enterprise.objects.all(), many=True)

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'recruits', 'logo', 'summary')


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'label_name')


class QuestionsSerializer(serializers.ModelSerializer):
    labels = serializers.StringRelatedField(many=True)
    replytime = serializers.CharField(allow_null=True)
    replyname = serializers.CharField(allow_null=True)

    class Meta:
        model = Question
        fields = ('id', 'createtime', 'labels', 'reply', 'replyname',
                  'replytime', 'title', 'unuseful_count', 'useful_count',
                  'user', 'visits')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class SubsSerializer(serializers.ModelSerializer):
    user = UserSerializer(label='用户', many=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'createtime', 'useful_count',
                  'unuseful_count', 'user')


class AnswerQuestionSerializer(serializers.ModelSerializer):
    subs = SubsSerializer(label='用户', many=True)
    user = UserSerializer(label='用户', many=True)

    class Meta:
        model = Reply
        fields = ('id', 'content', 'createtime', ' useful_count', 'problem',
                  'unuseful_count', 'subs', 'user', 'parent')


class UserCollectedArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title',)


class UserCollectedSerializer(serializers.ModelSerializer):
    articles = UserCollectedArticlesSerializer(label='收藏的文章', many=True)
    fans = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'articles', 'fans')


class CollectedArticlesSerializer(serializers.ModelSerializer):
    user = UserCollectedSerializer(label='我的收藏')
    collected_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'createtime', 'user', 'collected_users',
                  'collected', 'image')


class ContentTypeSerializer(serializers.ModelSerializer):
    '''接收的信息'''
    labels = LabelsSerializer(label='标签', many=True, allow_null=True)
    questions = QuestionsSerializer(label='我的问题', many=True, allow_null=True)
    answer_question = AnswerQuestionSerializer(label='我的回答', many=True, allow_null=True)
    collected_articles = CollectedArticlesSerializer(label='我的收藏', many=True, allow_null=True)
    enterpises = EnterpisesSimpleSerializer(label='具体职务', many=True, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'mobile', 'realname', 'birthday', 'sex', 'avatar', 'website',
                  'email', 'city', 'address', 'labels', 'questions', 'answer_question', 'collected_articles',
                  'enterpises')







class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    '''接收的信息'''
    # labels = LabelsSerializer(label='标签', many=True, allow_null=True)
    # questions = QuestionsSerializer(label='我的问题', many=True, allow_null=True)
    # answer_question = AnswerQuestionSerializer(label='我的回答', many=True, allow_null=True)
    # collected_articles = CollectedArticlesSerializer(label='我的收藏', many=True, allow_null=True)
    # enterpises = EnterpisesSimpleSerializer(label='具体职务', many=True, allow_null=True)
    birthday = serializers.DateField(format='%Y-%m-%d', allow_null=True)

    class Meta:
        model = User
        # fields = ('id', 'mobile', 'realname', 'birthday', 'sex', 'avatar', 'website',
        #           'email', 'city', 'address', 'labels', 'questions', 'answer_question', 'collected_articles',
        #           'enterpises')
        fields = ('id', 'mobile', 'realname', 'birthday', 'sex', 'avatar', 'website',
                  'email', 'city', 'address',)

    def validate_mobile(self, value):
        """针对mobile字段的内容进行补充验证"""
        mobile = value
        # 手机号格式
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式不正确')

        # 手机号是否注册
        return value

    def update(self, instance, validated_data):
        mobile = validated_data['mobile']

        count = User.objects.filter(mobile=mobile).count()

        if mobile != instance.mobile:

            if count != 0:
                raise serializers.ValidationError('手机号已注册')

        User.objects.filter(id=instance.id).update(**validated_data)

        return instance










# 修改密码
class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '最小长度为8',
                    'max_length': '最大长度为20'
                }
            }
        }

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))

        instance.save()
        print('ojbk')

        return instance
