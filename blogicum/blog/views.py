from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def index(request):
    # Получаем 5 последних опубликованных постов
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    # Получаем пост по ID, проверяем условия публикации
    post = get_object_or_404(
        Post,
        pk=id,
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    # Получаем категорию по slug, проверяем, что она опубликована
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    # Получаем посты для этой категории
    post_list = Post.objects.filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True
    ).order_by('-pub_date')
    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)
