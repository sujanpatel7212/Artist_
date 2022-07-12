# Generated by Django 4.0.3 on 2022-03-30 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_book_artist_artist_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_artist',
            name='artist_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book_artist',
            name='event_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book_artist',
            name='event_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book_artist',
            name='event_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book_artist',
            name='event_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book_artist',
            name='event_venue',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book_artist',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
