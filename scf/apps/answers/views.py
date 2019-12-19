from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from answers.models import Label, Question
from answers.serializers import LabelSerializer, QuestionsNewSerializer


class LabelView(ListAPIView):
    serializer_class = LabelSerializer
    queryset = Label.objects.all()
    pagination_class = None


class QuestionsNewView(ListAPIView):
    '''最新回答的问题'''
    serializer_class = QuestionsNewSerializer
    queryset = Question.objects.all()
    pagination_class = None
    # 排序
    filter_backends = [OrderingFilter]
    # 指定排序字段
    ordering_fields = ('updatetime', 'useful_count')


class QuestionsDoesNotAnswerView(ListAPIView):
    serializer_class = QuestionsNewSerializer

    def get_queryset(self):
        questions = Question.objects.filter(reply=0)
        return questions

    pagination_class = None


