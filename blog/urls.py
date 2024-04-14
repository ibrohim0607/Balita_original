from django.urls import path
from .views import index_view, about_view, category_view, contact_view, blog_detail_view

urlpatterns = [
    path('', index_view),
    path('about/', about_view),
    path('category/', category_view),
    path('contact/', contact_view),
    path('blog/<int:pk>/', blog_detail_view)
]
