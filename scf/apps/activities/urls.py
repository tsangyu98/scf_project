from django.conf.urls import url
from activities.views import ActivitiesView, DetailActivitiesView, UserGatheringView

urlpatterns = [
    url(r'^gatherings/$', ActivitiesView.as_view()),
    url(r'^gatherings/(?P<pk>\d+)/$', DetailActivitiesView.as_view()),
    url(r'^gatherings/(?P<pk>\d+)/join/$', UserGatheringView.as_view()),
]
