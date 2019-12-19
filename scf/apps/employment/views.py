from rest_framework.views import APIView
from django.shortcuts import render


# Create your views here.


# GET /recruits/search/latest/
class NewPositionInfoView(APIView):
    """获取最新的招聘信息列表"""

    def get(self, request):
        pass
