import json

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, CreateAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from toutiao.models import Channel, Article, Comment
from toutiao.serializers import HeadlineChannelSerializer, ArticleSerializer, ArticleDetailsSerializer, \
    ArticleSearchSerializer, CommentArticleSerializer, ArticleCommentSerializer, DetailsArticleSerializer


class HeadlineChannelView(ListAPIView):

    # def get(self, request):
    #     queryset = Channel.objects.all()
    #
    #     serializer = HeadlineChannelSerializer(queryset, many=True)
    #
    #     return Response(serializer.data)
    serializer_class = HeadlineChannelSerializer

    queryset = Channel.objects.all()


class ArticleListView(ListAPIView):


    serializer_class = ArticleSerializer

    def get_queryset(self, *args, **kwargs):

        id = self.kwargs['pk']
        if id == '-1':
            try:
                articles = Article.objects.all()
            except Article.DoesNotExist:
                raise Http404
        else:
            try:
                articles = Article.objects.filter(channel=id)
            except Article.DoesNotExist:
                raise Http404
        return articles

    # def list(self, request, *args, **kwargs):
    #     # 过滤
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # 分页
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     # 序列化
    #     serializer = self.get_serializer(queryset, many=True)
    #
    #     user = self.request.user
    #     redis_conn = get_redis_connection('like')
    #
    #     collect_data = redis_conn.get('collect_%s' % user.id)
    #
    #     # if collect_data:
    #     #     serializer.data['results'].append({'collected': True})
    #     # else:
    #     #     serializer.data['results'].append({'collected': False})
    #     return Response(serializer.data)

class CollectOrCancelArticle(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ArticleCommentSerializer

    queryset = Article.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.request.user
        redis_conn = get_redis_connection('like')
        collect_data = redis_conn.get('collect_%s' % user.id)
        if collect_data:
            redis_conn.delete('collect_%s' % user.id)
            instance = self.get_object()
            request.data['collected'] = False
            # instance.collected_users.user_id.delete()
            # instance.collected_users.save()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data={"message": "取消收藏成功", "success": False}
            return Response(data)
        else:
            redis_conn.set('collect_%s' % user.id, 'like')
            instance = self.get_object()
            request.data['collected'] = True
            request.data['collected_users'] = user.id
            # instance.collected_users.save()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {"message": "收藏成功", "success": True}
            return Response(data)

    # def put(self, request, pk):
    #
    #     user =request.user
    #     redis_conn = get_redis_connection('like')
    #
    #     collect_data = redis_conn.get('collect_%s' % user.id)
    #
    #     if collect_data:
    #         redis_conn.delete('collect_%s' % user.id)
    #         try:
    #             article = Article.objects.get(pk=pk)
    #         except Article.DoesNotExist:
    #             raise Http404
    #         article.collected = False
    #         article.collected_users.delete(user_id=user.id)
    #         article.save()
    #     # if not collect_data:
    #     #
    #     #     redis_conn.setex('collect_%s' % user.id, 'like')
    #         data = {"message": "取消收藏成功", "success": False}
    #
    #         return Response(data)
    #     else:
    #         collect_data = redis_conn.setex('collect_%s' % user.id, 'like')
    #         try:
    #             article = Article.objects.get(pk=pk)
    #         except Article.DoesNotExist:
    #             raise Http404
    #         article.collected = True
    #         article.collected_users.add(user.id)
    #         article.save()
    #         article.collected_users.save()
    #         data = {"message": "收藏成功", "success": True}
    #         return Response(data)






class ArticleDetails(RetrieveAPIView):
    serializer_class = ArticleDetailsSerializer
    # 指定视图所使用的查询集
    queryset = Article.objects.all()

    # def get(self, request, pk):
    #     """
    #     获取指定图书
    #     """
    #     instance = self.get_object()
    #
    #     # 将图书数据进行序列化
    #     serializer = ArticleDetailsSerializer(instance)
    #
    #     return Response(serializer.data)


class ReleaseArticle(GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DetailsArticleSerializer
    queryset = Article.objects.all()

    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        serializer = DetailsArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        article_id = serializer.data['id']
        return Response({"articleid": article_id,
                         'message': '发布成功',
                         'success': True})
    # def post(self, request, *args, **kwargs):
    #     serializer = DetailsArticleSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 反序列化-数据保存(save内部会调用序列化器类的create方法)
    #     serializer.save()
    #
    #     article_id = serializer.data['id']
    #
    #     data = {"articleid": article_id, "message": "发布成功", "success": True}
    #
    #     return Response(data)
    # permission_classes = [IsAuthenticated]
    #
    # serializer_class = ArticleReleaseSerializer
    # # 指定视图所使用的查询集
    # queryset = Article.objects.all()


class CommentArticle(APIView):

    def post(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            raise Http404

        serializer = CommentArticleSerializer(comment, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        data = {"message": "发布成功", "success": True}

        return Response(data)

class KeywordSearch(ListAPIView):
    serializer_class = ArticleSearchSerializer

    def get_queryset(self, *args, **kwargs):

        text = self.request.query_params.get('text')

        if not text:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(Q(title__contains=text) | Q(content__contains=text))

        return articles

    def list(self, request, *args, **kwargs):
        text = self.request.query_params.get('text')
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        serializer.data['results'].append({'text': text})
        return Response(serializer.data)
    # def get(self, request):
    #     """
    #     获取普通用户数据:
    #     1. 获取keyword关键字
    #     2. 查询普通用户数据
    #     3. 将用户数据序列化并返回
    #     """
    #     text = request.query_params.get('text')
    #
    #     if not text:
    #         articles = Article.objects.all()
    #     else:
    #         articles = Article.objects.filter(Q(title__contains=text) | Q(content__contains=text))
    #
    #     # 3. 将用户数据序列化并返回
    #     serializer = ArticleSearchSerializer(articles, many=True)
    #     serializer.data['results'].append({'text': text})
    #     return Response(serializer.data)

