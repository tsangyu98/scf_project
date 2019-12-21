from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from employment.models import Enterprise

class Collectenterprise(APIView):
    # authentication_classess = [BasicAuthentication]
    # 指定当前视图自己的权限控制方案，不再使用全局权限控制方案
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):

        user = request.user
        enterprise = Enterprise.objects.get(id=pk)
        enterprise.users.add(user)

        data = {'message':'收藏成功','success':True}
        return Response(data)