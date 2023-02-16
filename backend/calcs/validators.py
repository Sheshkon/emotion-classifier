import os
from django.core.exceptions import ValidationError
valid_extensions = ('.jpg', 'png', 'jpeg',)


def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1]
    if not extension.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
