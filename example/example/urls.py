from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^step1/', views.MyProcess.as_views()),
    url(r'^step2/', views.MyProcess2.as_views(namespace='bar')),
]
