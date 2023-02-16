from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

from services.recognition.recognition import get_faces_emotions


@login_required()
def index(request):
    ctx = {}
    response = get_faces_emotions(settings.STATIC_ROOT + '/img/img.jpg')
    ctx["image"] = response
    return render(request, 'index.html', ctx)
