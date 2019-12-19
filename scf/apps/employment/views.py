from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render


# Create your views here.


# GET /recruits/search/recommend/
from employment.models import Recruit
from employment.serializer import RecruitSerializer


class NewPositionInfoView(APIView):
    """获取最新的招聘信息列表"""

    def get(self, request):
        queryset = Recruit.objects.all()

        #序列化所有招聘信息
        serializer = RecruitSerializer(queryset,many=True)

        return Response(serializer.data)
