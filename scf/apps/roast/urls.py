
from django.conf.urls import url

from roast.views import SpitApiView, SpitapiView, SpitChildrenView,  UpdatethumbupView1, \
    CollectView1

urlpatterns = [
url(r'^spit/$',SpitApiView.as_view()),
url(r'^spit/(?P<pk>\d+)/$',SpitapiView.as_view()),
url(r'^spit/(?P<pk>\d+)/children/$',SpitChildrenView.as_view()),
url(r'^spit/(?P<pk>\d+)/updatethumbup/$',UpdatethumbupView1.as_view()),#点赞
url(r'^spit/(?P<pk>\d+)/collect/$',CollectView1.as_view()),#收藏
]