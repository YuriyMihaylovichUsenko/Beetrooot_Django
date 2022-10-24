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
    name_en = models.CharField(max_length=50, null=True, default="")
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50, null=True, default="")
    foto = models.ImageField(upload_to='images.authors')


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50, null=True, default="")
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name


class Article(models.Model):
    base_url = models.URLField()
    title = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500, null=True, default='')
    slug = models.SlugField(max_length=500, unique=True)
    description = models.TextField(default='')
    description_en = models.TextField(default='', null=True)
    text = models.TextField(default='')
    text_en = models.TextField(default='', null=True)
    tags = models.ManyToManyField(Tag, related_name='article')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    date_news = models.DateTimeField(null=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    comment = models.TextField(default='', max_length=1000)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='comments')
    date_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name