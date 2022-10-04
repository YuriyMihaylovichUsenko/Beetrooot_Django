from newspaper.models import Article, Image, Tag


def main():
    Article.objects.all().delete()
    Image.objects.all().delete()
    Tag.objects.all().delete()


if __name__ == '__main__':
    main()
