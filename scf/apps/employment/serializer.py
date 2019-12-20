from rest_framework import serializers

from employment.models import Recruit, Enterprise, City
from users.models import User


class CitySerializer(serializers.ModelSerializer):
    """城市信息序列化器类"""

    class Meta:
        model = City

        fields = '__all__'


class HotenterpriseSerializer(serializers.ModelSerializer):
    # 关联对象的嵌套序列化
    # recruits =RecruitIdSerializer(label='公司招聘岗位', many=True)
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'logo', 'summary', 'recruits')


class EnterpriseSerializer(serializers.ModelSerializer):
    """企业信息序列化器类"""

    class Meta:
        model = Enterprise

        fields = ('id', 'name', 'labels', 'logo', 'summary', 'recruits')


class RecruitSerializer(serializers.ModelSerializer):
    """招聘信息序列化器类"""

    # 关联对象嵌套序列化
    enterprise = EnterpriseSerializer(label='企业信息')

    class Meta:
        model = Recruit

        exclude = ("address", "state", "detailcontent", "detailrequire", "users", 'visits')


class EnterpriseInfoSerializer(serializers.ModelSerializer):
    """企业详情序列化器类"""

    recruits = RecruitSerializer(many=True)

    class Meta:
        model = Enterprise

        fields = ('id', 'recruits', 'name', 'summary', 'content', 'city',
                  'address', 'labels', 'coordinate', 'logo', 'url', 'visits', 'users')
