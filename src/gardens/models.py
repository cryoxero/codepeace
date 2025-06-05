from django.db import models
from django.core.exceptions import ValidationError
from os.path import splitext
from django.core.validators import MinValueValidator, MaxValueValidator

def validate_file_extension(value):
    ext = splitext(value.name)[1]
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}')

class Garden(models.Model):

    title = models.CharField(max_length=256, null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)
    initial_code = models.TextField(null=False, blank=False, default='')
    test_input = models.FileField(upload_to='garden_test/%Y/%m/%d/%H/%M/%S/', validators=[validate_file_extension], default='', unique=True)
    test_output = models.FileField(upload_to='garden_test/%Y/%m/%d/%H/%M/%S/', validators=[validate_file_extension], default='', unique=True)
    rating = models.IntegerField(null=False, blank=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    slug = models.SlugField(max_length=256, unique=True, blank=False, default='')
    runner = models.CharField(max_length=512, null=False, blank=False)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    approved = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.title
