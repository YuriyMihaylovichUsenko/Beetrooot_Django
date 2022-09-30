from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    base_url = models.URLField()

    def __str__(self):
        return self.image.url


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Article(models.Model):
    base_url = models.URLField()
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    text = models.CharField(max_length=10000, default='')

    image = models.ManyToManyField(Image, related_name='article')
    categories = models.ManyToManyField(Category, related_name='article')

    def __str__(self):
        return self.title
