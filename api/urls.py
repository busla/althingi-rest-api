from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #url(r'^sessions/$', views.SessionList.as_view()),
    #url(r'^sessions/(?P<pk>[0-9]+)/$', views.SessionDetail.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)