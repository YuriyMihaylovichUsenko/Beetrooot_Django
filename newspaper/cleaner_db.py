from newspaper.models import Article, Image, Tag, Category
import os

def main():
    Article.objects.all().delete()
    Image.objects.all().delete()
    Tag.objects.all().delete()
    Category.objects.all().delete()

    dir_ = 'd:\python_projects\Beetroot_Django\media\images'
    for f in os.listdir(dir_):
        os.remove(os.path.join(dir_, f))


if __name__ == '__main__':
    main()
