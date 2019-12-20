from rest_framework.response import Response
from rest_framework.views import APIView

from employment.models import Enterprise
from employment.serializeres.enterprisedetails import EnterpriseSerializer


class Enterprise1DetailView(APIView):
    """获取最新的招聘信息列表"""
    def get(self, request,pk):
        # queryset = Recruit.objects.get(id=pk)
        queryset = Enterprise.objects.get(id=pk)
        #序列化所有招聘信息
        serializer = EnterpriseSerializer(queryset)
        return Response(serializer.data)