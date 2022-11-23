from calendar import c
from distutils.command.upload import upload
from itertools import product
from django.db import models
from django.contrib.auth import get_user_model

from apps.computer.models import Laptop

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    laptop = models.ForeignKey(
        to=Laptop,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comments_images', blank=True, null=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.product.title}'
        