from rest_framework import serializers

from employment.models import Recruit, Enterprise, City


class RecruitSerializer(serializers.ModelSerializer):
    """招聘信息序列化器类"""

    class Meta:
        model = Recruit

        # exclude = ('detailcontent', 'detailrequire', 'visits')
        fields = '__all__'


class EnterpriseSerializer(serializers.ModelSerializer):
    """企业信息序列化器类"""

    class Meta:
        model = Enterprise

        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    """城市信息序列化器类"""

    class Meta:
        model = City

        fields = '__all__'
