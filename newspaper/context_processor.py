from .models import Category


def category_all(request):
    category = Category.objects.all()
    return {'categories': category}
