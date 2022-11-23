from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from django.urls import reverse

from .utils import get_time


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, primary_key=True, blank=True)
    parent_category = models.ForeignKey(
        verbose_name='Родительская категория',
        to='self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Laptop(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, primary_key=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    in_stock =  models.BooleanField(default=False)
    image = models.ImageField(upload_to='laptops_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    processor = models.CharField(max_length=250)
    video_card = models.CharField(max_length=250)
    ram = models.CharField(max_length=250)
    ssd = models.CharField(max_length=250, blank=True, null=True)
    hhd = models.CharField(max_length=250, blank=True, null=True)
    monitor = models.CharField(max_length=250)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='laptops')
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='laptops'
    )

    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        if not self.slug:
            self.slug = slugify(self.title +get_time())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('laptop-detail', kwargs={'pk': self.pk})


class LaptopImage(models.Model):
    image = models.ImageField(upload_to='laptops_images')
    laptop = models.ForeignKey(
        to=Laptop,
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self) -> str:
        return f'Image to {self.product.title}'

        
class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        blank=True,
        null=True
    )
    laptop = models.ForeignKey(
        to=Laptop,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self):
        return str(self.rating)


class Like(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    laptop = models.ForeignKey(
        to=Laptop,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    def __str__(self) -> str:
        return f'Liked by {self.user.username}'