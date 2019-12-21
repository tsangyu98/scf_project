from django.shortcuts import render

# Create your views here.
from django import http
from django.http import Http404
from django.shortcuts import render
import logging

from django_redis import get_redis_connection

logger=logging.getLogger('django')
from django.views import View
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from roast.models import Spit
from roast.serializers import SpitModelSerializer, SpitTModelSerializer, SpitCModelSerializer
from rest_framework import pagination

class SpitApiView(ListCreateAPIView):
    '''吐槽列表和发布吐槽'''
    # permission_classes = None
    pagination_class = None
    queryset = Spit.objects.all()
    serializer_class = SpitModelSerializer


    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            self.request.data['userid'] = user.id
            self.request.data['nickname'] = user.nickname
            self.request.data['avatar'] = user.avatar
            pid=int(request.data.get('parent'))
            # self.request.data['parent'] =pid

            if  pid :
                try:
                    spit=Spit.objects.get(id=pid)
                    spit.comment+=1
                except Exception as e:
                    raise Http404
            # self.request.data['userid']=2
            # self.request.data['nickname']='狗屎'
            # self.request.data['avatar']='12313'
        # super().create(self,request,*args, **kwargs)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SpitapiView(RetrieveAPIView):
    '''获取详细信息'''
    queryset = Spit.objects.all()
    serializer_class = SpitModelSerializer

# class CollectApiView(APIView):
#     '''收藏或取消收藏'''
#     def get(self,request,pk):
#         split= Spit.objects.get(id=pk)
#

class SpitChildrenView(APIView):
    '''获取吐槽评论'''

    def get(self,request,pk):
        try:
            spit = Spit.objects.filter(parent_id=pk)
        except Exception as e:
            raise  Http404
        serializer = SpitModelSerializer(spit,many=True)
        return Response(serializer.data)




# class CollectView(View):
#     '''添加收藏'''
#
#     # permission_classes =
#     def put(self,request,pk):
#         user = request.user
#         try:
#             count=Collect.objects.get(user_id=user.id,collect_id=pk)
#         except Exception as e :
#             logger.info(e)
#             count=None
#         try:
#             spit = Spit.objects.get(id=pk)
#         except Exception as e:
#             return http.HttpResponse(status=404)
#         if count:
#             spit.collected=(1-spit.collected)
#             # spit.save()
#             count.delete()
#         else:
#             spit.collected=True
#             # spit.save()
#             try:
#
#                 coment = Approval.objects.create(
#                     user=user,
#                     collect=spit
#                 )
#             except Exception as e:
#                 logger.error(e)
#                 return http.HttpResponse(status=404)
#
#
#         spit.save()
#
#
#         return http.JsonResponse({
#             'message':spit.message,
#             'success':True
#         })
#
#
#         # spit.thumbup += 1
#
#
# class UpdatethumbupView(View):
#     '''添加点赞'''
#
#     # permission_classes =
#     def put(self, request, pk):
#         user = request.user
#         try:
#             user =  Approval.objects.get(user_id=user.id,collect_id=pk)
#         except Exception as e:
#             logger.info(e)
#         try:
#             spit = Spit.objects.get(id=pk)
#         except Exception as e:
#             return http.HttpResponse(status=404)
#         if user:
#             spit.hasthumbup = (1 - spit.hasthumbup)
#             user.delete()
#         else:
#             spit.hasthumbup = True
#             try:
#
#                 coment =  Approval.objects.create(
#                     user=user,
#                     collect=spit,
#                 )
#             except Exception as e:
#                 return http.HttpResponse(status=404)
#         if spit.hasthumbup == True:
#             spit.thumbup += 1
#         else:
#             spit.thumbup -= 1
#
#         spit.save()
#
#         return http.JsonResponse({
#             'message': spit.message,
#             'success': True
#         })
################################reidas版本##################################
class CollectView1(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        user=request.user

        user_id =1
        try:
            spit = Spit.objects.get(id=pk)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        redis_conn = get_redis_connection('roast')
        spit_id=redis_conn.lrange('collect%s'%user_id,0,-1)

        list=[i.decode() for i in spit_id]
        if pk not in list:
            redis_conn.lpush('collect%s'%user_id,user_id)
            request.data['collected']=True
        else:
            redis_conn.lrem('collect%s'%user_id,0,user_id )
            request.data['collected'] = True
        serializer=SpitTModelSerializer(spit,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



class UpdatethumbupView1(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        user=request.user
        user_id=user.id
        try:
            spit = Spit.objects.get(id=pk)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        redis_conn = get_redis_connection('roast')
        spit_id=redis_conn.lrange('hasthumbup%s'%user_id,0,-1)
        list = [i.decode() for i in spit_id]
        if pk not in spit_id:
            spit_id = redis_conn.lpush('hasthumbup%s'%user_id,user_id)
            request.data['collected'] = True
            request.thumbup = spit.thumbup + 1

        else:
            spit_id = redis_conn.lrem('hasthumbup%s'%user_id,0,user_id )
            request.data['collected'] = True
            request.data['thumbup'] = spit.thumbup - 1
        serializer=SpitCModelSerializer(spit,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

