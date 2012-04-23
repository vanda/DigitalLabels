from django.db import models
from sorl.thumbnail import ImageField
# Create your models here.

class DigitalLabel(models.Model):
    """
    A label describing an individual object
    """
    name = models.CharField(max_length=255, null=False, blank=True)

    date_text = models.CharField(max_length=255, null=False, blank=True)
    artist_maker = models.CharField(max_length=255, null=False, blank=True)
    materials_techniques = models.CharField(max_length=255, null=False,
                                                            blank=True)
    museum_number = models.CharField(max_length=255, null=False, blank=True)
    object_number = models.CharField(max_length=16, null=False, blank=False,
                                     unique=True,
                                     help_text="""Unique "O" number, For 
                                             example, O9138, as used on
                                         Search the Collections""")
    credit_line = models.CharField(max_length=255, null=False, blank=True)
    main_text = models.TextField(blank=True)
    redownload = models.BooleanField(help_text="""WARNING: This may
                                         replace your existing content""")
    def __unicode__(self):
        if self.museum_number:
            return u"%s %s (%s)" % (self.object_number,
                                 self.name, self.museum_number)
        else:
            return self.name



class CMSLabel(models.Model):

    date = models.CharField(max_length=255, null=False)
    text = models.TextField()
    digitallabel = models.ForeignKey(DigitalLabel)

    def __unicode__(self):
        return u"%s for %s" % (self.date, self.digitallabel.museum_number)

class Image(models.Model):

    image_id = models.CharField(max_length=16, null=False)
    caption = models.CharField(max_length=255, null=False)
    digitallabel = models.ForeignKey(DigitalLabel)
    image_file = ImageField(upload_to="labels/images")

    def __unicode__(self):
        return u"%s for %s" % (self.image_id, self.digitallabel.museum_number)

class Group(models.Model):

    name = models.CharField(max_length=255, null=False)
    digitallabels = models.ManyToManyField(DigitalLabel)

from django.db.models.signals import pre_save, post_save
from labels.signals import get_cms_labels, get_api_data

pre_save.connect(get_api_data, DigitalLabel)
post_save.connect(get_cms_labels, DigitalLabel)


