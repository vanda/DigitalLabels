from django.db import models
# Create your models here.

class Label(models.Model):
    """
    A label describing an individual object
    """
    name = models.CharField(max_length=255, null=False, blank=True)
    date_text = models.CharField(max_length=255, null=False, blank=True)
    artist_maker = models.CharField(max_length=255, null=False, blank=True)
    object_number = models.CharField(max_length=16, null=False, blank=False)
    credit_line = models.CharField(max_length=255, null=False, blank=True)
    main_text = models.TextField(blank=True)
    redownload = models.BooleanField(help_text="WARNING: This may replace your exising content")

