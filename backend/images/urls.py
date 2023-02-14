from django.urls import path

from images import views

urlpatterns =[
    path('', views.index, name='index')
]
