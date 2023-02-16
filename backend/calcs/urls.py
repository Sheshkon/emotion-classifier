from django.urls import path

from calcs import views

urlpatterns = [
    path('image', views.upload_image, name='calcs-image')
]
