from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.client_register, name='register'),
    path('login/', views.client_login, name='login'),
    path('logout/', views.client_logout, name='logout'),
    path('home/', views.home_page, name='home_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('author/<int:author_id>/', views.author_page, name='author_page'),
    path('author/<int:author_id>/<str:book_title>/', views.book_page, name='book_page'),
    path('author/<int:author_id>/<str:book_title>/reviews', views.book_reviews, name='book_reviews'),
]
