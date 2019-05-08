from django.db import models


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    author_ip = models.GenericIPAddressField(default='127.0.0.0')
    created_date = models.DateTimeField(auto_now_add=True)
    done_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

