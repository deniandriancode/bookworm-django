from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64, blank=True)
    genre = models.CharField(max_length=32, blank=True)
    num_of_page = models.PositiveIntegerField(default=0)
    release_year = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0.0)
    is_public_domain = models.BooleanField(default=False)
    note = models.CharField(max_length=800, blank=True)

    def __str__(self):
        return self.title
