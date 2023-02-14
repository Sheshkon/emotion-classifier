from django.shortcuts import render

from services.recognition.recognition import get_faces_emotions


def index(request):
    ctx = {}
    response = get_faces_emotions('backend/static/img/img.png')
    ctx["image"] = response

    return render(request, 'index.html', ctx)
