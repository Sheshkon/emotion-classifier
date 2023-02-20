from django.contrib import admin

from calcs.models import ImageClassifier


class ImageClassifierAdmin(admin.ModelAdmin):
    exclude = ('output_info',)


admin.site.register(ImageClassifier, ImageClassifierAdmin)
