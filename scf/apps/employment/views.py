import json
from django.http import Http404
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from employment.models import Recruit, City, Enterprise
from employment.models import Recruit, City, Enterprise
from employment.serializer import RecruitSerializer, CitySerializer, HotenterpriseSerializer, EnterpriseInfoSerializer


# GET /recruits/search/recommend/
class RecommendInfoView(ListAPIView):
    """获取推荐的招聘信息列表"""

    def get(self, request):
        queryset = Recruit.objects.all()
        serializer_class = RecruitSerializer
        # 排序
        filter_backends = [OrderingFilter]

        # 指定排序字段
        ordering_fields = ('createtime',)
        # # 序列化所有招聘信息
        # serializers = RecruitSerializer(queryset, many=True)
        # return Response(serializers.data)
# GET /recruits/search/recommend/
class NewPositionInfoView(APIView):
    """获取最新的招聘信息列表"""
    def get(self, request):
        queryset = Recruit.objects.all()
        # 序列化所有招聘信息
        serializer = RecruitSerializer(queryset, many=True)

        return Response(serializer.data)


class HostCityView(APIView):
    '''热门城市展示'''

    def get(self, request):
        queryset = City.objects.filter(ishot=1)
        serializer = CitySerializer(queryset, many=True)

        return Response(serializer.data)


class HotenterpriseView(APIView):
    '''热门公司'''

    def get(self, request):
        # 获取对象
        queryset = Enterprise.objects.all()
        # 数据序列化返回
        serializer = HotenterpriseSerializer(queryset, many=True)

        return Response(serializer.data)


# POST /recruits/search/city/keyword/
class SearchPositionView(APIView):
    """搜索某个职位"""

    def post(self, request):
        # 反序列化-数据校验

        json_dict = json.loads(request.body.decode())
        city = json_dict.get('cityname')
        keyword = json_dict.get('keyword')

        queryset = Recruit.objects.filter(city=city, jobname__contains=keyword)

        serializer = RecruitSerializer(queryset, many=True)

        return Response(serializer.data)


# GET /enterprise/{id}/
class EnterpriseInfoView(APIView):
    """获取企业详情信息"""

    def get(self, request, id):
        # 获取对象
        queryset = Enterprise.objects.get(id=id)

        # 序列化数据返回
        serialiser = EnterpriseInfoSerializer(queryset)

        return Response(serialiser.data)


# POST /recruits/{id}/collect/
class CollectionPositionView(APIView):
    """收藏或者取消收藏职位"""
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        # 判断用户是否收藏
        user = request.user  #得到用户
        get = Recruit.objects.get(id=id)   #通过id得到对应工作

        list = [get.id for get in get.users.all()]    #get.users.all()得到作业的收藏者的id ，get.id遍历取到一个id
        # 判断当前登录id 在不在上面列表里
        if user.id not in list:   #不在添加
            get.users.add(user)    #get.users.add(user)  多对多添加收藏
            return Response({'message': '收藏成功', 'success': True})
        else:   #在取消收藏
            try:
                get.users.remove(user)    #get.users.remove(user)   多对多添加收藏
                return Response({'message': '取消收藏', 'success': True})
            except Exception as e:
                return Http404
