from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client_info', views.client_info, name='client_info')
]
