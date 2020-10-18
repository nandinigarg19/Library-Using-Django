from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^searchBook/$', views.searchBook, name='book-search'),
    re_path(r'^searchAuthor/$', views.searchAuthor, name='author-search')

]