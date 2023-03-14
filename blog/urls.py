from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, \
    toggle_publish

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('read/<int:pk>/', ArticleDetailView.as_view(), name='read'),
    path('update/<int:pk>/', ArticleUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete'), # deprecated
    path('publish/<int:pk>/', toggle_publish, name='publish'),
]