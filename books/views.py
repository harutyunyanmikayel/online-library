from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from .models import Client, Book, Author, Reservation, BookReview
from django.utils import timezone
from django.urls import reverse


def client_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'books/register.html', {'error_message': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'books/register.html', {'error_message': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'books/register.html', {'error_message': 'Email is already registered'})

        user = User.objects.create_user(first_name=name, last_name=surname, username=username, email=email,
                                        password=password1)
        user.save()

        client = Client.objects.create(user=user, address=address)
        client.save()

        email_sender(user)

        messages.add_message(request, messages.SUCCESS, 'Your have registered successfully!')

        return redirect('login')

    else:
        return render(request, 'books/register.html')


def client_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f'Welcome, {request.user.first_name}!')
            return redirect('home_page')
        else:
            return render(request, 'books/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'books/login.html')


def client_logout(request):
    logout(request)
    return redirect('home_page')


def home_page(request):
    authors = Author.objects.all()

    query = request.GET.get('query')

    if query:
        books = Book.objects.filter(title__icontains=query)

    elif query == '':
        return redirect(reverse('home_page'))

    else:
        books = []

    return render(request, 'books/home.html', {'authors': authors, 'books': books, 'query': query})


def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        from_email = settings.EMAIL_HOST_USER
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = ['djangolibraryuser@gmail.com']

        full_message = (f"Name: {name}\n"
                        f"email: {email}\n\n"
                        f"{message}")

        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=True,)

            messages.add_message(request, messages.SUCCESS,
                                 'Your form has been sent! We will get back to you as soon as possible.')

        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Failed to submit your form.')

        return HttpResponseRedirect(request.path)

    return render(request, 'books/contact.html')


def author_page(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    books = Book.objects.filter(author=author)
    review_count_list = []

    for book in books:
        review_count = len(BookReview.objects.filter(book=book))
        review_count_list.append(review_count)

    books_with_reviews = zip(books, review_count_list)

    return render(request, 'books/author.html', {'author': author, 'books_with_reviews': books_with_reviews})


def book_page(request, author_id, book_title):
    book = get_object_or_404(Book, title=book_title)
    reservation = None

    if request.method == 'POST':
        client = get_object_or_404(Client, user=request.user)

        if 'confirm_booking' in request.POST:
            reservation = Reservation.objects.create(book=book, client=client,
                                                     expiration_date=timezone.now() + timezone.timedelta(days=30))
            reservation.save()
            book.is_available = False
            book.save()

            messages.add_message(request, messages.SUCCESS, 'Your book is reserved!')

        elif 'cancel_booking' in request.POST:
            reservation = Reservation.objects.get(book=book)
            reservation.delete()

            messages.add_message(request, messages.SUCCESS, 'Your have canceled your booking.')

        return HttpResponseRedirect(request.path)

    else:
        try:
            reservation = Reservation.objects.get(book=book)

        except Reservation.DoesNotExist:
            pass

    return render(request, 'books/book.html', {'book': book, 'reservation': reservation})


def book_reviews(request, author_id, book_title):
    book = get_object_or_404(Book, title=book_title)
    reviews = BookReview.objects.filter(book=book)
    has_reviewed = False

    if not request.user.is_anonymous:
        client = get_object_or_404(Client, user=request.user)
        if BookReview.objects.filter(client=client, book=book).exists():
            has_reviewed = True

    if request.method == 'POST':
        if 'submit_review' in request.POST:
            submit_review(request, book, client)

        elif 'delete_review' in request.POST:
            book_review = BookReview.objects.get(client=client, book=book)
            book_review.delete()

            messages.add_message(request, messages.SUCCESS, 'Your review hes been deleted successfully.')

        return HttpResponseRedirect(request.path)

    return render(request, 'books/reviews.html', {'book': book, 'reviews': reviews, 'has_reviewed': has_reviewed})


def submit_review(request, book, client):
    review = request.POST.get('review')
    rating = request.POST.get('rating')

    try:
        book_review = BookReview.objects.create(
            client=client,
            book=book,
            review=review,
            rating=rating
        )
        book_review.save()

        messages.add_message(request, messages.SUCCESS, 'Review submitted successfully!')
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Something went wrong trying to submit the review.')


def email_sender(user):
    subject = "Congratulations!"
    message = "Welcome to our Library! Here you can find a lot of interesting books."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Error sending email: {e}')
