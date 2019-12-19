from rest_framework import serializers

from employment.models import Recruit, Enterprise, City

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

class HotenterpriseSerializer(serializers.ModelSerializer):
    #关联对象的嵌套序列化
    # recruits =RecruitIdSerializer(label='公司招聘岗位', many=True)
    class Meta:
        model = Enterprise
        fields =('id','name','labels','logo','summary','recruits')

class RecruitSerializer(serializers.ModelSerializer):
    """招聘信息序列化器类"""
    enterprise=HotenterpriseSerializer(many=True)

    class Meta:
        model = Recruit
        # exclude = ('detailcontent', 'detailrequire', 'visits')
        fields = ('id','jobname','salary','condition','education','type','city','createtime','enterprise','labels')