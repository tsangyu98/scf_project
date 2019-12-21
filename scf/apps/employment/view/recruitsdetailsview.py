from rest_framework.response import Response
from rest_framework.views import APIView
from employment.models import Recruit
from employment.serializeres.recruitsdetails import RecruitSerializer


class RecruitDetailView(APIView):
    """获取最新的招聘信息列表"""
    def get(self, request,pk):

        # queryset = Recruit.objects.get(id=pk)
        queryset = Recruit.objects.get(id=pk)
        #序列化所有招聘信息
        serializer = RecruitSerializer(queryset)
        return Response(serializer.data)