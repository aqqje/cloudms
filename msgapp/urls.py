from django.urls import path
from  msgapp import views

urlpatterns = [
    path('', views.msgproc)
]