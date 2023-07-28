from datetime import timezone
from django.db import models
from django.contrib.auth import get_user_model as User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.utils.crypto import get_random_string
from django_mysql.models import ListCharField
from .variables import *


# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(User(), on_delete=models.CASCADE)
    event_id = models.CharField(unique=True, blank=True, max_length=10, editable=False)
    staff = models.CharField(default="[]", blank=True, null=True, max_length=1400)
    title = models.CharField(verbose_name="enter the event name",max_length=200,)
    qr_code = models.ImageField(upload_to='event_qr_code', blank=True)
    location = models.CharField(verbose_name='event location', max_length=200, null=True)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    eventstartdate = models.DateField(null=True, blank=True)
    eventenddate = models.DateField(null=True, blank=True)
    starttime = models.TimeField(null=True, blank=True)
    endtime = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.event_id or self.event_id == "":
            self.event_id = get_random_string(length=10)
        
        if not self.qr_code:
            qr_img = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr_img.add_data(f"{HostName}/api/event/{self.event_id}/ticket/create/")
            qr_img.make(fit=True)
            
            img = qr_img.make_image(fill_color="black", back_color="white")
            size = len(qr_img.get_matrix())
            
            canvas = Image.new('RGB', (size*10, size*10), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(img)
            fname = f'Event-{self.title}-{str(self.event_id)}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save(*args, **kwargs)
    
class Ticket(models.Model):
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User(), on_delete=models.CASCADE)
    ticket_id = models.CharField(unique=True, blank=True, max_length=10, editable=False)
    qr_code = models.ImageField(upload_to='ticket_qr_code', blank=True)
    created_at = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    attended = models.BooleanField(default=False,)
    
    def __str__(self):
        return str(self.Event)
    
    def save(self, *args, **kwargs):
        if not self.ticket_id or self.ticket_id == "":
            self.ticket_id = get_random_string(length=10)
            
        if not self.qr_code:
            qr_img = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr_img.add_data(f"{self.ticket_id}")
            qr_img.make(fit=True)
            
            img = qr_img.make_image(fill_color="black", back_color="white")
            size = len(qr_img.get_matrix())
            
            canvas = Image.new('RGB', (size*10, size*10), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(img)
            fname = f'Ticket-{self.user}-{str(self.ticket_id)}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
            super().save(*args, **kwargs)
        if not self.expiry_date:
            self.expiry_date = self.Event.eventenddate
        super().save(*args, **kwargs)