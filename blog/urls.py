from django.urls import path
from .views import index_view, about_view, category_view, contact_view, category_detail_view,blog_search_view


urlpatterns = [
    path('', index_view),
    path('blog/', category_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('blog/<int:pk>/', category_detail_view),
    path('search/', blog_search_view, name='search_results'),
]
