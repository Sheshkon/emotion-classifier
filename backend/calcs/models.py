from django.db import models


class ImageClassifier(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='calcs_images')
    input = models.ImageField(upload_to='image_classifier/')
    input_binary = models.BinaryField()
    output = models.ImageField(upload_to='image_classifier')
    output_binary = models.BinaryField()
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return str(self.profile) + '(' + str(self.date_time) + ')'
