from django.core.exceptions import ValidationError

def validate_image_size(image):
    file_size = image.file.size
    limit_mb = 1
    if file_size > limit_mb * (1024 * 1024):
        raise ValidationError('File Size Must be below {0} MB'.format(limit_mb))