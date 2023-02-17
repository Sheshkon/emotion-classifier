from django.db import models


class ImageClassifier(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='calcs_images')
    input = models.ImageField(upload_to='image_classifier/')
    output = models.ImageField(upload_to='image_classifier')
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField(null=True, blank=True)
    output_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.profile) + '(' + str(self.date_time) + ')'
