from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review, Author
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def index(request):
    books = Book.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    return render(request, 'books/index.html', {'books': books, 'query': query})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        if 'comment' in request.POST:
            comment = request.POST['comment']
            try:
                rating = float(request.POST.get('rating', 0.0))
            except ValueError:
                rating = 0.0
            review = Review(book=book, user=request.user, comment=comment, rating=rating)
            review.save()
            return redirect('book_detail', book_id=book.id)
        elif 'title' in request.POST:
            book.title = request.POST['title']
            book.content = request.POST['content']
            try:
                book.rating = float(request.POST.get('rating', 0.0))
            except ValueError:
                book.rating = 0.0
            if request.FILES.get('image'):
                book.image = request.FILES['image']
            book.save()
            return redirect('book_detail', book_id=book.id)
    
    return render(request, 'books/book_detail.html', {'book': book})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.content = request.POST['content']
        try:
            book.rating = float(request.POST.get('rating', 0.0))
        except ValueError:
            book.rating = 0.0
        if request.FILES.get('image'):
            book.image = request.FILES['image']
        book.save()
        return redirect('book_detail', book_id=book.id)
    return render(request, 'books/book_detail.html', {'book': book, 'edit_mode': True})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    books = author.books.all()
    return render(request, 'books/author_detail.html', {'author': author, 'books': books})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to BookRating.')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'books/register.html', {'form': form})