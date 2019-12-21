from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from users import views
from users.views import ChangeUserPassword, UserInfoView

urlpatterns = [

    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SMSCodeView.as_view()),
    # url(r'^authorizations/$', views.AdminAuthorizeView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^users/$', views.RegisterSerializer.as_view()),
    url(r'^users/like/(?P<pk>\d+)/$', views.Follow.as_view()),
    url(r'^user/password/$', ChangeUserPassword.as_view()),
    url(r'^user/$', UserInfoView.as_view()),

]