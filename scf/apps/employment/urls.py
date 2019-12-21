from django.conf.urls import url
from employment.view.enterprisecollectview import Collectenterprise
from employment.view.recruitsdetailsview import RecruitDetailView
from employment.view.visitview import EnterpriseVisitAdd, RecruitVisitAdd
from employment.views import *
urlpatterns = [
    url(r'^recruits/search/latest/$', NewPositionInfoView.as_view()),
    url(r'^recruits/search/recommend/$', NewPositionInfoView.as_view()),
    url(r'^city/hotlist/$', HostCityView.as_view()),
    url(r'^enterprise/search/hotlist/$', HotenterpriseView.as_view()),
    url(r'^recruits/search/city/keyword/$', SearchPositionView.as_view()),
    url(r'^enterprise/(?P<id>\d+)/$', EnterpriseInfoView.as_view()),
    url(r'^recruits/(?P<id>\d+)/collect/$', CollectionPositionView.as_view()),
    url(r'^recruits/(?P<id>\d+)/cancelcollect/$', CollectionPositionView.as_view()),
    url(r'^enterprise/(?P<pk>\d+)/visit/$',EnterpriseVisitAdd.as_view()),
    url(r'^recruits/(?P<pk>\d+)/visit/$',RecruitVisitAdd.as_view()),
    url(r'^recruits/(?P<pk>\d+)/$',RecruitDetailView.as_view()),
    url(r'^enterprise/(?P<pk>\d+)/collect/$',Collectenterprise.as_view()),
    url(r'^enterprise/(?P<id>\d+)/cancelcollect/$',CollectionPositionView.as_view()),
]
