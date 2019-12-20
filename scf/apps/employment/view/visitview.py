from rest_framework.response import Response
from rest_framework.views import APIView
from employment.models import Enterprise, Recruit
from employment.serializeres.visvtserializer import EnterpriseSerializer


class EnterpriseVisitAdd(APIView):

    def put(self,request,pk):
        '''修改企业浏览'''
        try:
            #得到访问对象
            enterprise =Enterprise.objects.get(id=pk)
        except:
            raise 404
        serializer=EnterpriseSerializer(enterprise,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #返回参数
        data ={"message":"更新成功","success":True}
        return Response(data)

class RecruitVisitAdd(APIView):

    def put(self,request,pk):
        '''增加职位访问次数'''
        try:
            #得到访问对象
            recruit =Recruit.objects.get(id=pk)
        except:
            raise 404
        serializer=EnterpriseSerializer(recruit,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        #返回参数
        data ={"message":"更新成功","success":True}
        return Response(data)




