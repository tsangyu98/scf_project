from rest_framework import serializers
from employment.models import Enterprise, Recruit


# class ES(object):
#     """用户类"""
#     def __init__(self, message, success):
#         self.success = success
#         self.message = message
#
# class ReturnSerializer(serializers.Serializer):
#     """序列化器类"""
#     message = serializers.CharField(read_only=True)
#     success = serializers.CharField(read_only=True)
class EnterpriseSerializer(serializers.ModelSerializer):
    """企业信息序列化器类"""
    class Meta:
        model = Enterprise
        exclude =("users",)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        visits = instance.visits + 1
        instance.visits = validated_data.get('visits', visits)
        instance.save()
        return instance

class RecruitSerializer(serializers.ModelSerializer):
    """增加职位访问次数"""
    # 关联对象嵌套序列化
    # enterprise = EnterpriseSerializer(label='企业信息')
    class Meta:
        model = Recruit

        exclude = ("users",)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        visits = instance.visits + 1
        instance.visits = validated_data.get('visits', visits)
        instance.save()
        return instance