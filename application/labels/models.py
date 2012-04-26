import urllib2
from django.conf import settings
from django.db import models
from django.utils import simplejson
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

    __museumobject_json = None

    @property
    def museumobject_json(self):

        if self.__museumobject_json == None:
            item_url = 'http://%s/api/json/museumobject/%s/' % (
                                        settings.COLLECTIONS_API_HOSTNAME,
                                        self.object_number)
            try:
                response = urllib2.urlopen(item_url)
                self.__museumobject_json = simplejson.load(response)[0]

            except urllib2.HTTPError, e:
                if e.code == 404:
                    # Missing object
                    pass
                else:
                    # other error
                    pass

        return self.__museumobject_json

    def create_cms_labels(self):

        museum_object = self.museumobject_json
        if museum_object:
            for l in museum_object['fields']['labels']:
                cms_label = CMSLabel()
                cms_label.date = l['fields']['date']
                cms_label.text = l['fields']['label_text']
                cms_label.digitallabel = self
                cms_label.save()

    def create_images(self):

        museum_object = self.museumobject_json
        if museum_object:
            for i in museum_object['fields']['image_set']:
                image_id = i['fields']['image_id']
                try:
                    image_url = \
                        'http://%s/media/thira/collection_images/%s/%s.jpg' % \
                            (settings.MEDIA_SERVER, image_id[:6], image_id)
                    response = urllib2.urlopen(image_url)
                    cms_image = Image()
                    cms_image.image_id

                except urllib2.HTTPError, e:
                    if e.code == 404:
                        # Missing object
                        pass
                    else:
                        # other error
                        pass

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
from labels.signals import get_api_data, get_related_api_data

pre_save.connect(get_api_data, DigitalLabel)
post_save.connect(get_related_api_data, DigitalLabel)


