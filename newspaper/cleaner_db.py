from newspaper.models import Article, Image, Tag, Category
import os

def main():
    Article.objects.all().delete()
    Image.objects.all().delete()
    Tag.objects.all().delete()
    Category.objects.all().delete()

    dir_ = 'd:\python_projects\Beetroot_Django\media\images\\articles'
    for f in os.listdir(dir_):
        os.remove(os.path.join(dir_, f))

    dir_2 = 'd:\python_projects\Beetroot_Django\media\images\\authors'
    for f in os.listdir(dir_):
        os.remove(os.path.join(dir_2, f))

if __name__ == '__main__':
    main()
