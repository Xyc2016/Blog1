from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Article(models.Model):
    title = models.TextField()
    text = models.TextField()
    show = models.BooleanField()
    pub_date = models.DateTimeField('date published')
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    visitor = models.TextField()

    def __str__(self):
        return self.text
