from rest_framework import serializers
from employment.models import Enterprise, Recruit


class Enterprise1Serializer1(serializers.ModelSerializer):
    """企业信息序列化器类"""
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'logo', 'summary', 'recruits')


class EnterpriseRecruitSerializer1(serializers.ModelSerializer):
    '''2成 职位'''
    enterprise = Enterprise1Serializer1(label='企业信息')
    class Meta:
        model = Recruit
        # fields ='__all__'
        fields = ('id', 'enterprise', 'jobname', 'salary', 'condition', 'education', 'type', 'city',  'createtime', 'labels')


class EnterpriseSerializer(serializers.ModelSerializer):
    """企业信息序列化器类"""
    recruits = EnterpriseRecruitSerializer1(label='企业岗位信息',many=True)
    class Meta:
        model = Enterprise
        fields= ('id','recruits','name','summary','content','city','address','labels','coordinate','logo','url','visits','users')
