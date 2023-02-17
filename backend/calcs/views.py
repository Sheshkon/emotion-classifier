import base64

from django.shortcuts import render
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from calcs.forms import ImageClassifierFrom
from calcs.models import ImageClassifier
from accounts.models import Profile

from services.recognition.recognition import get_faces_emotions


@login_required()
def upload_image(request):
    form = ImageClassifierFrom()
    last_instance = ImageClassifier.objects.filter(profile__pk=request.user.id).last()
    input_file = None
    output_file = None

    if last_instance:
        input_file = last_instance.input
        output_file = last_instance.output

    if request.method == "POST":
        form = ImageClassifierFrom(request.POST, request.FILES)

        if form.is_valid():
            image_classifier = form.save(commit=False)
            image_classifier.profile = Profile.objects.get(pk=request.user.id)
            image_classifier.save()

            input_file = image_classifier.input
            b64_encode = get_faces_emotions(settings.MEDIA_ROOT + '/' + input_file.name)

            image_classifier.output.save('output.jpg', ContentFile(base64.b64decode(b64_encode)))
            output_file = image_classifier.output

    return render(request, 'upload_img.html', {'form': form,
                                               'input': input_file.url if input_file else None,
                                               'output': output_file.url if output_file else None})
