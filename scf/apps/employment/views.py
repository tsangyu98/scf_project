from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
# GET /recruits/search/latest/
from employment.models import Recruit, City, Enterprise
from employment.serializer import RecruitSerializer, CitySerializer, HotenterpriseSerializer


class HostCityView(APIView):
    '''热门城市展示'''
    def get(self,request):
        queryset = City.objects.filter(ishot=1)
        serializer =CitySerializer(queryset,many=True)

        return Response(serializer.data)

class NewPositionInfoView(APIView):
    """获取最新的招聘信息列表"""

    def get(self, request):
        queryset = Recruit.objects.all()

        #序列化所有招聘信息
        serializer = RecruitSerializer(queryset,many=True)

        return Response(serializer.data)

class HotenterpriseView(APIView):
    '''热门公司'''
    def get(self,request):
        #获取对象
        queryset=Enterprise.objects.filter(id=2)
        #数据序列化返回
        serializer =HotenterpriseSerializer(queryset,many=True)

        return Response(serializer.data)

