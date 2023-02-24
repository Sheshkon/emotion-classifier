from django.urls import path
from calcs.views import HistoryImageClassifier, upload_image, live_camera


urlpatterns = [
    path('image/', upload_image, name='calcs-image'),
    path('image-history/', HistoryImageClassifier.as_view(), name='image-history'),
    path('camera', live_camera, name='calcs-live-camera'),
]
