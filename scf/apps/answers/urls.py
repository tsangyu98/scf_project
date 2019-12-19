from django.conf.urls import url

from answers.views import LabelView, QuestionsNewView, QuestionsDoesNotAnswerView

urlpatterns = [
    url('^labels/$', LabelView.as_view()),
    url(r'^questions/-1/label/new/$', QuestionsNewView.as_view()),
    url(r'^questions/-1/label/hot/$', QuestionsNewView.as_view()),
    url(r'^questions/-1/label/wait/$', QuestionsDoesNotAnswerView.as_view()),
]
