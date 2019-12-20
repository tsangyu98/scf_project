from rest_framework import serializers
from employment.models import Recruit, Enterprise

class Enterprise1Serializer(serializers.ModelSerializer):
    """企业信息序列化器类"""
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'logo', 'summary', 'recruits')

class EnterpriseRecruitSerializer(serializers.ModelSerializer):
    enterprise=Enterprise1Serializer(label='企业信息')
    class Meta:
        model = Recruit
        fields= ('id','jobname','salary','condition','education','type','city','createtime','enterprise','labels')

class EnterpriseSerializer(serializers.ModelSerializer):
    """企业信息序列化器类"""
    recruits = EnterpriseRecruitSerializer(label='企业岗位信息',many=True)
    class Meta:
        model = Enterprise
        fields= ('id','recruits','name','summary','content','city','address','labels','coordinate','logo','url','visits','users')

class RecruitSerializer(serializers.ModelSerializer):
    """招聘信息序列化器类"""
    # 关联对象嵌套序列化
    enterprise = EnterpriseSerializer(label='企业信息')
    class Meta:
        model = Recruit
        # fields ='__all__'
        fields= ('id','enterprise','jobname','salary','condition','education','type','city','address','state','createtime','labels','detailcontent','detailrequire','visits','users')
