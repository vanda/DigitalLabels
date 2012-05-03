import logging
import os
import urllib2
from django.conf import settings
from django.db import models
from django.utils import simplejson
from django.utils.safestring import mark_safe
from sorl.thumbnail import ImageField, get_thumbnail
# Create your models here.
# import the logging library

# Get an instance of a logger
logger = logging.getLogger('labels')


class Group(models.Model):

    name = models.CharField(max_length=255, null=False)

    def __unicode__(self):

        return self.name


class DigitalLabel(models.Model):
    """
    A label describing an individual object
    """
    name = models.CharField(max_length=255, null=False, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)
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
    primary_image = models.ForeignKey("Image", null=True, blank=True,
                                      related_name="primary_for")
    gateway_object = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        if self.museum_number:
            return u"%s %s (%s)" % (self.object_number,
                                 self.name, self.museum_number)
        else:
            return self.name

    _museumobject_json = None
    _thumbnail_url = None

    @property
    def thumbnail_url(self):

        if not self._thumbnail_url:

            if self.image_set.count() > 1:

                if self.primary_image:
                    image_file = self.primary_image
                else:
                    image_file = self.image_set.all()[0]

                im = get_thumbnail(image_file.local_file_name, '100x100',
                                                    quality=85, pad=True)

                self._thumbnail_url = im.url

        return self._thumbnail_url


    def thumbnail_tag(self):

        return mark_safe('<img alt="%s" src="%s" />' % (
                                            self.name, self.thumbnail_url))

    thumbnail_tag.allow_tags = True
    thumbnail_tag.short_description = 'Thumb'


    @property
    def museumobject_json(self):

        if self._museumobject_json == None:
            item_url = 'http://%s/api/json/museumobject/%s/' % (
                                        settings.COLLECTIONS_API_HOSTNAME,
                                        self.object_number)
            try:
                response = urllib2.urlopen(item_url)
                self._museumobject_json = simplejson.load(response)[0]

            except urllib2.HTTPError, e:
                if e.code == 404:
                    # Missing object
                    pass
                else:
                    # other error
                    pass

        return self._museumobject_json

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
                    cms_image, cr = Image.objects.get_or_create(
                                digitallabel=self, image_id=image_id)
                    cms_image.store_vadar_image()
                    cms_image.caption = image_id
                    cms_image.image_file = os.path.join(
                                    cms_image.image_file.field.upload_to,
                                    unicode(cms_image.image_id) + '.jpg')
                    if image_id == museum_object['fields']['primary_image_id']:
                        self.primary_image = cms_image
                    cms_image.save()

                except urllib2.HTTPError, e:
                    if e.code == 404:
                        # Missing object
                        pass
                    else:
                        # other error
                        pass
            self.save()


class CMSLabel(models.Model):

    date = models.CharField(max_length=255, null=False)
    text = models.TextField()
    digitallabel = models.ForeignKey(DigitalLabel)

    def __unicode__(self):
        return u"%s for %s" % (self.date, self.digitallabel.museum_number)


class Image(models.Model):

    image_id = models.CharField(max_length=16, null=False)
    caption = models.CharField(max_length=255, null=False)
    image_file = ImageField(upload_to="labels/images")
    position = models.PositiveIntegerField(null=False, default=0)
    digitallabel = models.ForeignKey(DigitalLabel)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return u"%s for %s" % (self.image_id, self.digitallabel.museum_number)

    @property
    def local_file_name(self):
        """Where should this image be stored if it can be retrieved?"""
        if self.image_id:
            return "%s%s/%s.jpg" % (settings.MEDIA_ROOT,
                                        self.image_file.field.upload_to,
                                         unicode(self.image_id))
        else:
            raise Exception('No Image ID set')

    def store_vadar_image(self):
        #create the url and the request
        image_url = 'http://%s/media/thira/collection_images/%s/%s.jpg' % \
                     (settings.MEDIA_SERVER, self.image_id[:6], self.image_id)
        req = urllib2.Request(image_url)

        # Open the url
        try:
            logging.info("downloading " + image_url)
            f = urllib2.urlopen(req)
            meta = f.info()
            if meta.type == 'image/jpeg':
                # Open our local file for writing
                local_file = open(self.local_file_name, "wb")
                #Write to our local file
                local_file.write(f.read())
                local_file.close()
                return True
            else:
                logging.error("Image Error: Wrong type %s" % (meta.type))
                return False
        #handle errors
        except urllib2.HTTPError, e:
            logging.error("HTTP Error: %s %s" % (e.code, image_url))
            return False
        except urllib2.URLError, e:
            logging.error("URL Error: %s %s" % (e.reason, image_url))
            return False


from django.db.models.signals import pre_save, post_save
from labels.signals import get_api_data, get_related_api_data, \
                                                        create_thumbnails

pre_save.connect(get_api_data, DigitalLabel)
post_save.connect(get_related_api_data, DigitalLabel)
post_save.connect(create_thumbnails, Image)
