from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^login/$', views.user_login, name='user_login'),
]
urlpatterns2 = [
    url(r'^idioms/$', views.IdiomList.as_view()),
]
urlpatterns += format_suffix_patterns(urlpatterns2)
