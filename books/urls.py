from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('authors/', views.author_list, name='author_list'),
    path('about/', views.about, name='about'),
    path('review/<int:review_id>/reply/', views.reply_review, name='reply_review'),
    path('notifications/', views.notifications, name='notifications'),
]