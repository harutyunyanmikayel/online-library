from django.contrib import admin
from .models import (Client, Author, Book, Reservation, BookReview)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_available')
    list_filter = ('author', 'is_available')
    search_fields = ('title', 'author__name')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client_username', 'book', 'reserved_date', 'expiration_date')
    list_filter = ('book__author',)
    search_fields = ('client_username', 'book__title')

    def client_username(self, obj):
        return obj.client.user.username

    client_username.short_description = 'Username'


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('client_username', 'book', 'rating')
    list_filter = ('rating', 'book')
    search_fields = ('book__title', 'book__author__name')

    def client_username(self, obj):
        return obj.client.user.username

    client_username.short_description = 'Username'


admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Client)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Reservation, ReservationAdmin)
