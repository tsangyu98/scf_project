from rest_framework import serializers
from activities.models import Gathering
from users.models import User


class UserActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )


class ActivitiesSerializer(serializers.ModelSerializer):
    '''
    活动序列化器类
    '''
    users = UserActivitiesSerializer(many=True)

    class Meta:
        model = Gathering
        fields = ('id', 'name', 'image', 'city', 'starttime', 'endrolltime', 'users')




class DetailActivitiesSerializer(serializers.ModelSerializer):
    '''
    活动详情数据
    '''

    users = UserActivitiesSerializer()

    class Meta:
        model = Gathering
        fields = '__all__'
