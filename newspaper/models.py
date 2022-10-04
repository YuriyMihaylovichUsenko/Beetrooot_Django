from django.db import models


class Image(models.Model):
    article = models.ForeignKey(
        'newspaper.Article',
        on_delete=models.CASCADE,
        related_name='images',
        null=True
    )
    image = models.ImageField(upload_to='images')
    base_url = models.URLField()

    def __str__(self):
        return self.image.url



class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name


class Article(models.Model):
    base_url = models.URLField()
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    text = models.TextField(default='')
    tags = models.ManyToManyField(Tag, related_name='article')

    def __str__(self):
        return self.title
