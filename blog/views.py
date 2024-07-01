import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Contact, Comment, Category
from django.db.models import Count


def index_view(request):
    page = request.GET.get("page", 1)
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).order_by('created_at')
    more_blog_posts = Post.objects.filter(is_published=True).order_by('-created_at')
    page_obj = Paginator(posts, 6)
    post_list = Post.objects.annotate(comment_count=Count('comment')).filter(
        comment_count__gt=0).order_by('-comment_count')

    d = {
        'posts': page_obj.page(page),
        'more_blog_posts': more_blog_posts,
        'categories': categories.annotate(total=Count('post')),
        'post_list': post_list,
        'home': 'active'
    }

    return render(request, 'index.html', context=d)


def contact_view(request):
    post_list = Post.objects.annotate(comment_count=Count('comment')).filter(
        comment_count__gt=0).order_by('-comment_count')
    categories = Category.objects.all()
    d = {
        'post_list': post_list,
        'categories': categories.annotate(total=Count('post')),
        'contact': 'active'

    }
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data.get('name'), email=data.get('email'),
                                     write_message=data.get('message'),
                                     phone=data.get('phone'))
        obj.save()
        # token = "6912718237:AAH2v2r4x2TuYnHqfpbi1ci43AxYKEiBWoE"
        # requests.get(
        #     f"""https://api.telegram.org/bot{token}/sendMessage?chat_id=5093765356&text=Balita\nid: {obj.id}\nname: {obj.name}\nemail: {obj.email}\nwrite_message: {obj.write_message}\nphone: {obj.phone}""")
        return redirect('/contact')
    return render(request, 'contact.html', context=d)


def about_view(request):
    post_list = Post.objects.annotate(comment_count=Count('comment')).filter(
        comment_count__gt=0).order_by('-comment_count')
    info = request.GET
    cat = info.get('cat')
    page = info.get("page", 1)
    if info.get('cat'):
        posts = Post.objects.filter(is_published=True, category_id=cat).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
    post_obj = Paginator(posts, 4)
    categories = Category.objects.all()
    d = {
        'posts': post_obj.page(page),
        'post_list': post_list,
        'categories': categories.annotate(total=Count('post')),
        'about': 'active'
    }

    return render(request, 'about.html', context=d)


def category_view(request):
    post_list = Post.objects.annotate(comment_count=Count('comment')).filter(
        comment_count__gt=0).order_by('-comment_count')
    data = request.GET
    cat = data.get("cat")
    page = data.get("page", 1)
    categories = Category.objects.all()
    if cat:
        posts = Post.objects.filter(is_published=True, category__id=cat).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_published=True).order_by('-created_at')

    page_obj = Paginator(posts, 6)

    return render(request, 'category.html',
                  context={'posts': page_obj.page(page), 'categories': categories.annotate(total=Count('post')),
                           'post_list': post_list,
                           'category': 'active'})


def blog_search_view(request):
    data = request.GET
    text = data.get('text', '')
    text = text.replace('+', ' ')
    if text:
        posts = Post.objects.filter(title__icontains=text)
    else:
        posts = Post.objects.all()
    return render(request, 'serach_results.html', context={'posts': posts, 'search_query': text, })


def blog_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = post.get_related_posts()
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(post_id=pk, name=data.get('name'), message=data.get('message'),
                                     email=data.get('email'))
        obj.save()
        return redirect(f'/blog/{pk}')
    comments = Comment.objects.filter(post_id=pk)
    d = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'categories': categories.annotate(total=Count('post')),
    }
    return render(request, 'blog-single.html', context=d)
