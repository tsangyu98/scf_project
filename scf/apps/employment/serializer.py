from rest_framework import serializers

from employment.models import Recruit, Enterprise, City
from users.models import User



class EnterpriseSerializer(serializers.ModelSerializer):
    """企业信息序列化器类"""

    class Meta:
        model = Enterprise

        fields = ('id', 'name', 'labels', 'logo', 'summary', 'recruits')


class CitySerializer(serializers.ModelSerializer):
    """城市信息序列化器类"""

    class Meta:
        model = City

        fields = '__all__'


class RecruitSerializer(serializers.ModelSerializer):
    """招聘信息序列化器类"""

    # 关联对象嵌套序列化
    enterprise = EnterpriseSerializer(label='企业信息')

    class Meta:
        model = Recruit

        exclude = ("address", "state", "detailcontent", "detailrequire", "users", 'visits')

