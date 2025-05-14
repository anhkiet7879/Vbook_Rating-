from django.contrib import admin
from django.urls import path, include
from books import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('admin/', admin.site.urls),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('accounts/', include('django.contrib.auth.urls')),  # Thêm URL cho authentication
    path('accounts/register/', views.register, name='register'),  # URL cho đăng ký
]