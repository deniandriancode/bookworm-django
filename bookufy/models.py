from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=128)
    num_of_page = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
