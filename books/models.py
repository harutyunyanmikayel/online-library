from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.author}"


class BookReview(models.Model):
    REVIEW_CHOICES = [
        ('Great', 'Great'),
        ('Good', 'Good'),
        ('Decent', 'Decent'),
        ('Bad', 'Bad'),
        ('Terrible', 'Terrible'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.CharField(max_length=500)
    rating = models.CharField(max_length=15, choices=REVIEW_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.username} | {self.book.title} | {self.rating}"


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.client.user.username} - {self.book.title}"

