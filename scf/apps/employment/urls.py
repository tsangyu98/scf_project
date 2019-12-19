from django.conf.urls import url
from employment.views import *

urlpatterns = [
    url(r'^recruits/search/latest/$',NewPositionInfoView.as_view()),
    url(r'^city/hotlist/$',HostCityView.as_view()),
]
