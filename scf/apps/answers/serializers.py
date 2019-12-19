from rest_framework import serializers
from answers.models import Label, Question


class LabelSerializer(serializers.ModelSerializer):
    '''获取所有标签序列化器类'''
    class Meta:
        model = Label
        fields = ('id', 'label_name')


class QuestionsNewSerializer(serializers.ModelSerializer):
    '''获取最新被回答过的问题'''
    class Meta:
        model = Question
        exclude = ('content', 'thumbup', 'solve', 'updatetime')


