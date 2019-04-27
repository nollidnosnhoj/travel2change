from django.core.exceptions import ValidationError

# Validate the max size of image
def validate_image_size(image):
    file_size = image.file.size
    limit_mb = 3
    if file_size > limit_mb * (1024 * 1024):
        raise ValidationError('File Size Must be below {0} MB'.format(limit_mb))
