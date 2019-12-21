from django.db import transaction
from rest_framework import serializers
from answers.models import Label, Question, Reply
from users.models import User


class LabelSerializer(serializers.ModelSerializer):
    """获取所有标签序列化器类"""

    class Meta:
        model = Label
        fields = ('id', 'label_name')


class QuestionsSerializer(serializers.ModelSerializer):
    """获取被回答过的问题序列化器类"""

    class Meta:
        model = Question
        exclude = ('content', 'thumbup', 'solve', 'updatetime')


class QuestionsPublicSerializer(serializers.ModelSerializer):
    """发布问题的序列化器类"""
    user_id = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ('content', 'labels', 'title', 'user_id')

    def validate(self, attrs):
        labels = attrs.get('labels')
        label_all = Label.objects.all()
        label_all = [label for label in label_all]

        for label in labels:
            if label not in label_all:
                raise serializers.ValidationError('label不对')
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            question = super().create(validated_data)
            return question


class QuestionsReplyUserSerializer(serializers.ModelSerializer):
    """获取回答用户序列化器类"""

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class CommentQuestionSubSerializer(serializers.ModelSerializer):
    """获取回答评论列表的序列化器类"""

    user = QuestionsReplyUserSerializer()
    subs = serializers.StringRelatedField()

    class Meta:
        model = Reply
        exclude = ('updatetime', 'type')


class CommentQuestionSerializer(serializers.ModelSerializer):
    """获取问题评论列表的序列化器类"""
    user = QuestionsReplyUserSerializer()

    class Meta:
        model = Reply
        fields = ('id', 'content', 'createtime', 'useful_count', 'problem', 'unuseful_count', 'user')


class ReplyQuestionSerializer(serializers.ModelSerializer):
    """获取问题回答列表的序列化器类"""
    subs = CommentQuestionSerializer(many=True)
    user = QuestionsReplyUserSerializer()

    class Meta:
        model = Reply
        exclude = ('updatetime', 'type')


class QuestionsAllSerializer(serializers.ModelSerializer):
    """获取问题详情的序列化器类"""
    user = serializers.StringRelatedField()
    comment_question = CommentQuestionSerializer(label='问题评论列表', many=True)
    answer_question = ReplyQuestionSerializer(label='问题回答列表', many=True)

    class Meta:
        model = Question
        exclude = ('updatetime', 'thumbup', 'solve')


class ReplySerializer(serializers.ModelSerializer):
    """回答问题的序列化器类"""
    user_id = serializers.IntegerField()

    class Meta:
        model = Reply
        fields = ('problem', 'content', 'type', 'parent','user_id')
        extra_kwargs = {
            'parent': {'required': False}
        }

    def validate(self, attrs):
        if attrs.get('type') == 1:
            parent = attrs.get('parent')
            parent_ids = [parent.id for parent in Reply.objects.all()]
            if parent is None:
                raise serializers.ValidationError('没有父级id')
            if parent not in parent_ids:
                raise serializers.ValidationError('父级id不正确')
        return attrs

    def create(self, validated_data):
        problem = validated_data.get('problem')
        content = validated_data.get('content')
        type = validated_data.get('type')
        user_id = validated_data.get('user_id')
        reply = Reply.objects.create(
            problem=problem,
            content=content,
            type=type,
            user_id=user_id
        )
        question = reply.problem
        question.reply += 1
        question.save()
        return reply




class QuestionlabelSerializer(serializers.ModelSerializer):
    labels = serializers.StringRelatedField(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Question
        exclude = ('thumbup', 'content', 'updatetime', 'solve')


class LabelDetailsSerializer(serializers.ModelSerializer):
    questions = QuestionlabelSerializer(many=True)

    class Meta:
        model = Label
        fields = '__all__'