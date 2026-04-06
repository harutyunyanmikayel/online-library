from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Reservation  # check_expired_reservations


@receiver(post_delete, sender=Reservation)
def update_book_availability(sender, instance, **kwargs):
    if instance.book:
        instance.book.is_available = True
        instance.book.save()


# @receiver(post_save, sender=Reservation)
# def schedule_expiration_check(sender, instance, **kwargs):
#     # Schedule the expiration check background task
#     check_expired_reservations(repeat=3600)
