from django.shortcuts import render
# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from activities.models import Gathering
from activities.serializers import ActivitiesSerializer, DetailActivitiesSerializer


class ActivitiesView(ListAPIView):
    '''活动视图'''

    queryset = Gathering.objects.all()
    serializer_class = ActivitiesSerializer


class DetailActivitiesView(RetrieveAPIView):
    queryset = Gathering.objects.all()
    serializer_class = DetailActivitiesSerializer


class UserGatheringView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            gather = Gathering.objects.get(id=pk)
        except:
            return Response({'message': '找不到活动', 'success': False})

        user = request.user
        gather.users.add(user)
        data = {'message': 'ok', 'success': True}
        return Response(data)
