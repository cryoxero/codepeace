from django.db import models

class Garden(models.Model):

    title = models.CharField(max_length=256, null=False, blank=False, unique=True)
    description = models.TextField(null=False, blank=False)
    initial_code = models.TextField(null=False, blank=False, default='')
    tests = models.JSONField(blank=False, null=False, default=dict)
    rating = models.IntegerField(null=False, blank=False, default=1)
    slug = models.SlugField(max_length=256, unique=True, blank=False, default='')
    runner = models.CharField(max_length=512, null=False, blank=False)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
