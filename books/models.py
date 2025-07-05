from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-book')  # FontAwesome icon class
    color = models.CharField(max_length=20, default='primary')  # Bootstrap color class
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='author_images/', null=True, blank=True)
    bio = models.TextField(blank=True, help_text="Tiểu sử tác giả")
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.FloatField(default=0.0)  # Rating trung bình từ các review
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg_rating = sum(review.rating for review in reviews) / reviews.count()
            self.rating = round(avg_rating, 1)
        else:
            self.rating = 0.0
        self.save()

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    rating = models.FloatField(default=0.0)  # Đánh giá cá nhân từ 0 đến 5
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_rating()

    def __str__(self):
        return f"Review by {self.user.username if self.user else 'Anonymous'} for {self.book.title}"

class WantToRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='want_to_read')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='want_to_read_users')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']  # Mỗi user chỉ có thể thêm một cuốn sách một lần

    def __str__(self):
        return f"{self.user.username} wants to read {self.book.title}"