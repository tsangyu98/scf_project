from django.db import transaction
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from answers.models import Label, Question, Reply
from answers.serializers import LabelSerializer, QuestionsSerializer, QuestionsPublicSerializer, QuestionsAllSerializer, \
    ReplySerializer, LabelDetailsSerializer


class LabelView(ListAPIView):
    """获取所有的标签列表视图类"""

    serializer_class = LabelSerializer
    queryset = Label.objects.all()
    pagination_class = None


class LabelUserApiView(APIView):

    def get(self, request):
        """用户关注的标签"""
        user = request.user
        queryset = user.labels.all()
        serializer = LabelSerializer(queryset, many=True)
        return Response(serializer.data)


class QuestionsNewView(ListAPIView):
    """最新回答的问题视图类"""
    serializer_class = QuestionsSerializer
    pagination_class = None
    # 排序
    filter_backends = [OrderingFilter]
    # 指定排序字段
    ordering_fields = ('updatetime', 'visits')

    def get_queryset(self):
        questions = Question.objects.exclude(reply=0)
        return questions


class QuestionsHotView(ListAPIView):
    """热门回答问题视图类"""
    serializer_class = QuestionsSerializer

    pagination_class = None
    # 排序
    filter_backends = [OrderingFilter]
    # 指定排序字段
    ordering_fields = ('reply',)

    def get_queryset(self):
        questions = Question.objects.exclude(reply=0)
        return questions


class QuestionsDoesNotAnswerView(ListAPIView):
    """待回答的问题视图类"""
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        questions = Question.objects.filter(reply=0)
        return questions

    pagination_class = None


class QuestionspublicView(GenericAPIView):
    """发布问题视图类"""
    serializer_class = QuestionsPublicSerializer
    queryset = Question.objects.all()

    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        serializer = QuestionsPublicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '发布成功',
                         'success': True})


class QuestionsDetailView(GenericAPIView):
    """问题详情视图类"""

    def get(self, request, pk):
        try:
            instance = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            raise serializers.ValidationError('pk不正确')

        question_comments = Reply.objects.filter(type=0, problem=instance)
        question_replys = Reply.objects.filter(type=2, problem=instance)

        for question_reply in question_replys:
            reply_comments = Reply.objects.filter(type=1, problem=instance, parent=question_reply)
            question_reply.subs = reply_comments
        instance.answer_question = question_replys
        instance.comment_question = question_comments

        question = QuestionsAllSerializer(instance)

        return Response(question.data)


class QuestionsUsefulView(APIView):
    """对问题有用的视图类"""

    def put(self, request, pk):
        with transaction.atomic():
            question = Question.objects.get(id=pk)
            question.useful_count += 1
            question.save()
        return Response({'message': 'ok',
                         'success': True})


class QuestionsUnusefulView(APIView):
    """对问题没用的视图类"""

    def put(self, request, pk):
        with transaction.atomic():
            question = Question.objects.get(id=pk)
            question.unuseful_count += 1
            question.save()
        return Response({'message': 'ok',
                         'success': True})


class QuestionsReplyView(APIView):
    """回答问题的视图类"""

    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        serializer = ReplySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReplyusefulView(APIView):
    """回答有用的视图类"""

    def put(self, request, pk):
        with transaction.atomic():
            reply = Reply.objects.get(id=pk)
            reply.useful_count += 1
            reply.save()
        return Response({'message': 'ok',
                         'success': True})


class ReplyUnusefulView(APIView):
    """回答无用的视图类"""

    def put(self, request, pk):
        redis_conn = get_redis_connection('label_user')
        label_user = redis_conn.get('answer_%s' % request.user.id)
        if label_user is not None:
            if label_user.decode() == pk:
                return Response({'message': '修改失败', 'success': False})
        reply = Reply.objects.get(pk=pk)
        reply.unuseful_count += 1
        reply.save()
        redis_conn.setex('answer_%s' % request.user.id, 3600 * 24, pk)
        return Response({'message': '修改成功', 'success': True})


class FocusinApiview(APIView):
    '''关注标签'''

    def put(self, request, pk):
        try:
            Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise serializers.ValidationError('pk不正确')
        try:
            request.user.labels.add(pk)
        except Exception as e:
            raise serializers.ValidationError('用户已关注')
        return Response({'message': '关注成功', 'success': True})


class FocusoutApiview(APIView):
    '''取消关注标签'''

    def put(self, request, pk):
        try:
            Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise serializers.ValidationError('pk不正确')
        request.user.labels.remove(pk)
        return Response({'message': '取消关注成功', 'success': True})


class LabelDetailsApiView(RetrieveAPIView):
    serializer_class = LabelDetailsSerializer
    queryset = Label.objects.all()
