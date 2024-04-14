import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Post, Contact, Comment, Tag


def index_view(request):
    info = request.GET
    cat = info.get('cat')
    page = info.get("page", 1)
    if info.get('cat'):
        posts = Post.objects.filter(is_published=True, tags__id=cat).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
    tags = Tag.objects.all()
    post_obj = Paginator(posts, 4)
    d = {
        'posts': post_obj.page(page),
        'popular_tags': Post.objects.filter(is_published=True).order_by('-tags'),
        'popular_posts': Post.objects.filter(is_published=True).order_by('comment'),
        'moreblogposts': Post.objects.filter(is_published=True).order_by('created_at'),
        'tags': tags

    }
    return render(request, 'index.html', context=d)


def contact_view(request):
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data.get('name'), email=data.get('email'),
                                     write_message=data.get('message'),
                                     phone=data.get('phone'))
        obj.save()
        token = "6912718237:AAH2v2r4x2TuYnHqfpbi1ci43AxYKEiBWoE"
        requests.get(
            f"""https://api.telegram.org/bot{token}/sendMessage?chat_id=5093765356&text=BALITA\nid: {obj.id}\nname: {obj.name}\nemail: {obj.email}\nmessage: {obj.write_message}\nphone: {obj.phone}""")

        return redirect('/contact')
    d = {
        'popular_posts': Post.objects.filter(is_published=True).order_by('comment'),
        'tags': Tag.objects.all()

    }
    return render(request, 'contact.html', context=d)


def about_view(request):
    info = request.GET
    cat = info.get('cat')
    page = info.get("page", 1)
    if info.get('cat'):
        posts = Post.objects.filter(is_published=True, category_id=cat).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
    post_obj = Paginator(posts, 4)
    tags = Tag.objects.all()
    d = {
        'posts': post_obj.page(page),
        'popular_posts': Post.objects.filter(is_published=True).order_by('comment'),
        'tags': tags
    }

    return render(request, 'about.html', context=d)


def category_view(request):
    return render(request, 'category.html')


def blog_detail_view(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(post_id=pk, name=data.get('name'), message=data.get('message'),
                                     email=data.get('email'))
        obj.save()
        return redirect(f'/blog/{pk}')
    comments = Comment.objects.filter(post_id=pk)
    d = {
        'post': post,
        # 'blogs': Post.objects.filter(is_published=True).first(),
        'popular_posts': Post.objects.filter(is_published=True).order_by('-comment'),
        'comments': comments,
        'tags': Tag.objects.all()
    }
    return render(request, 'blog-single.html', context=d)
