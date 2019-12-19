from django.conf.urls import url
from employment.views import *

urlpatterns = [
    url(r'^recruits/search/recommend/$',NewPositionInfoView.as_view())
]
