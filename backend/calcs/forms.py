from django import forms

from calcs.models import ImageClassifier


class ImageClassifierFrom(forms.ModelForm):
    class Meta:
        model = ImageClassifier
        fields = ['input', 'description']
