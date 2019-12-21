from rest_framework import serializers
from rest_framework.fields import BooleanField

from toutiao.models import Channel, Article, Comment
from users.models import User


class HeadlineChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel

        fields = ('id', 'name')


class ArticleSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title')


class UserSimpleSerializer(serializers.ModelSerializer):

    articles = ArticleSimpleSerializer(label='用户发布的文章', many=True)

    fans = serializers.PrimaryKeyRelatedField(label='粉丝', read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'nickname', 'avatar', 'articles', 'fans')


class ArticleSerializer(serializers.ModelSerializer):

    collected = serializers.SerializerMethodField()

    user = UserSimpleSerializer(label='文章作者')

    collected_users = serializers.PrimaryKeyRelatedField(label='收藏用户', read_only=True, many=True)

    class Meta:
        model = Article
        exclude = ('updatetime', 'thumbup', 'comment_count', 'labels')

    def get_collected(self, obj):
        user = self.context["request"].user
        print('user = ', user)
        collected_users = obj.collected_users.all()

        if user in collected_users:
            return True
        else:
            return False


class ArticleCommentSerializer(serializers.ModelSerializer):
    collected = serializers.SerializerMethodField()

    collected_users = serializers.PrimaryKeyRelatedField(label='收藏用户', read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('id', 'collected', 'collected_users')

    def get_collected(self, obj):
        user = self.context["request"].user
        print('user = ', user)
        collected_users = obj.collected_users.all()

        if user in collected_users:
            return True
        else:
            return False


class SubSimpleSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(label='文章作者')
    subs = serializers.StringRelatedField(label='父评论', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'updatetime': {'required': False}
        }


class CommentSimpleSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(label='文章作者')

    subs = SubSimpleSerializer(label='评论', many=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleDetailsSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(label='用户ID')

    collected = serializers.SerializerMethodField()

    collected_users = serializers.StringRelatedField(label='收藏用户', read_only=True, many=True)

    comments = CommentSimpleSerializer(label='问题ID', many=True)

    labels = serializers.PrimaryKeyRelatedField(label='标签', read_only=True, many=True)

    channel = serializers.PrimaryKeyRelatedField(label='频道', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

        # extra_kwargs = {
        #     'image': {'read_only': True}
        # }

    def get_collected(self, obj):
        user = self.context["request"].user
        print('user = ', user)
        collected_users = obj.collected_users.all()

        if user in collected_users:
            return True
        else:
            return False


class DetailsArticleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    labels = serializers.PrimaryKeyRelatedField(label='标签', read_only=True, many=True)

    channel = serializers.PrimaryKeyRelatedField(label='频道', read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'content', 'labels', 'title', 'channel', 'user_id')


class ArticleSearchSerializer(serializers.ModelSerializer):

    # text = serializers.CharField(label='关键字')

    class Meta:
        model = Article
        fields = ('id', 'createtime', 'content', 'title')


class CommentArticleSerializer(serializers.ModelSerializer):

    article = serializers.PrimaryKeyRelatedField(label='问题ID', read_only=True)

    parent = serializers.StringRelatedField(label='父评论', read_only=True)

    user = serializers.PrimaryKeyRelatedField(label='用户ID', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'content', 'parent', 'createtime', 'user')


