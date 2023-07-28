# Generated by Django 4.1.7 on 2023-07-28 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(blank=True, editable=False, max_length=10, unique=True)),
                ('staff', models.CharField(blank=True, default='[]', max_length=1400, null=True)),
                ('title', models.CharField(max_length=200, verbose_name='enter the event name')),
                ('qr_code', models.ImageField(blank=True, upload_to='event_qr_code')),
                ('location', models.CharField(max_length=200, null=True, verbose_name='event location')),
                ('description', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('eventstartdate', models.DateField(blank=True, null=True)),
                ('eventenddate', models.DateField(blank=True, null=True)),
                ('starttime', models.TimeField(blank=True, null=True)),
                ('endtime', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(blank=True, editable=False, max_length=10, unique=True)),
                ('qr_code', models.ImageField(blank=True, upload_to='ticket_qr_code')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('attended', models.BooleanField(default=False)),
                ('Event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.event')),
            ],
        ),
    ]
