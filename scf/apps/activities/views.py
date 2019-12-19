from django.shortcuts import render
# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from activities.models import Gathering
from activities.serializers import ActivitiesSerializer, DetailActivitiesSerializer


class ActivitiesView(ListAPIView):
    '''活动视图'''

    queryset = Gathering.objects.all()
    serializer_class = ActivitiesSerializer


class DetailActivitiesView(RetrieveAPIView):
    queryset = Gathering.objects.all()
    serializer_class = DetailActivitiesSerializer



