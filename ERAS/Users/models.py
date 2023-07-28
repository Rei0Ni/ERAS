from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


# Create your models here.
class CustomUser(AbstractUser):
    System_Admin = 1
    Organizer = 2
    Event_Staff =3
    Attendee = 4
    
    ROLE_CHOICES = (
        (System_Admin, 'Admin'),
        (Organizer, 'Organizer'),
        (Event_Staff, 'Staff'),
        (Attendee, 'Attendee'),
    )
    email = models.EmailField(unique=True, blank=True)
    secret_id = models.CharField(blank=False, null=False, max_length=10)
    role = models.PositiveSmallIntegerField(default=System_Admin, choices=ROLE_CHOICES, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.secret_id or self.secret_id == "":
            self.secret_id = get_random_string(length=10)
            
        super().save(*args, **kwargs)