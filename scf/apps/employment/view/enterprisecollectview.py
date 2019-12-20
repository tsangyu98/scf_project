from rest_framework.response import Response
from rest_framework.views import APIView
from employment.models import Enterprise

class Collectenterprise(APIView):
    def post(self,request,pk):

        user = request.user
        enterprise = Enterprise.objects.get(id=id)
        enterprise.users.add(user)

        data = {'message':'收藏成功','success':True}
        return Response(data)