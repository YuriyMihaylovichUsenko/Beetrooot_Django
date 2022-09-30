from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)


def category(request):
    context = {}
    return render(request, 'category-grid.html', context)


def single(request):
    context = {}
    return render(request, 'single.html', context)