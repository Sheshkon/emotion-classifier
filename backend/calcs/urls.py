from django.urls import path
from calcs.views import HistoryImageClassifier

from calcs import views

urlpatterns = [
    path('image/', views.upload_image, name='calcs-image'),
    path('image-history/', HistoryImageClassifier.as_view(), name='image-history'),
]
