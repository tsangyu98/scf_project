from django.conf.urls import url
from employment.views import *

urlpatterns = [
    url(r'^recruits/search/recommend/$',NewPositionInfoView.as_view()),
    url(r'^city/hotlist/$',HostCityView.as_view()),
    url(r'^enterprise/search/hotlist/$',HotenterpriseView.as_view()),

]
