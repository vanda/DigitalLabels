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


class DigitalLabel(models.Model):

    name = models.CharField(max_length=255, null=False)

    def __unicode__(self):

        return self.name


class Portal(models.Model):

    name = models.CharField(max_length=255, null=False)

    def __unicode__(self):

        return self.name


class MuseumObject(models.Model):
    """
    A label describing an individual object
    """
    name = models.CharField(max_length=255, null=False, blank=True)
    digitallabel = models.ForeignKey(DigitalLabel, null=True, blank=True,
                                                related_name="museumobjects")
    portal = models.ForeignKey(Portal, null=True, blank=True,
                                                related_name="museumobjects")
    date_text = models.CharField(max_length=255, null=False, blank=True)
    artist_maker = models.CharField(max_length=255, null=False, blank=True)
    place = models.CharField(max_length=255, null=False, blank=True)
    materials_techniques = models.CharField(max_length=255, null=False,
                                                            blank=True)
    museum_number = models.CharField(max_length=255, null=False, blank=True)
    object_number = models.CharField(max_length=16, null=False, blank=True,
                                     unique=True,
                                     help_text="""Unique "O" number, For
                                             example, O9138, as used on
                                         Search the Collections""")
    credit_line = models.CharField(max_length=255, null=False, blank=True)
    artfund = models.BooleanField(default=False)
    main_text = models.TextField(blank=True)
    redownload = models.BooleanField(help_text="""WARNING: This may
                                         replace your existing content""")
    gateway_object = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=False, default=1)

    class Meta:
        ordering = ['position']
        verbose_name = "object"

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

            if self.image_set.count() > 0:

                # images are sorted by priority, so take the first
                image_file = self.image_set.all()[0]

                im = get_thumbnail(image_file.local_filename, '44x44',
                                                    quality=85, pad=True)

                self._thumbnail_url = im.url

        return self._thumbnail_url

    def thumbnail_tag(self):

        if self.thumbnail_url:
            return mark_safe('<img alt="%s" src="%s" />' % (
                                            self.name, self.thumbnail_url))
        else:
            return mark_safe('<em>No Images</em>')

    thumbnail_tag.allow_tags = True
    thumbnail_tag.short_description = 'Thumb'

    @property
    def museumobject_json(self):

        if self._museumobject_json == None and self.object_number:
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
                cms_label.museumobject = self
                cms_label.save()

    def create_images(self):

        museum_object = self.museumobject_json
        if museum_object:
            for i in museum_object['fields']['image_set']:
                image_id = i['fields']['image_id']
                try:
                    cms_image, cr = Image.objects.get_or_create(
                                museumobject=self, image_id=image_id)
                    # retreive image from media server
                    image_success = cms_image.store_vadar_image()
                    if image_success:
                        cms_image.caption = image_id
                        cms_image.image_file = os.path.join(
                                        cms_image.image_file.field.upload_to,
                                        unicode(cms_image.image_id) + '.jpg')
                        if image_id == \
                                museum_object['fields']['primary_image_id']:
                            cms_image.position = 0
                        cms_image.save()
                    else:
                        cms_image.delete()

                except urllib2.HTTPError, e:
                    cms_image.image_file = ''
                    if e.code == 404:
                        # Missing object
                        pass
                    else:
                        # other error
                        pass


class TextLabel(models.Model):
    """
    A label describing biography or a historical notes
    """
    title = models.CharField(max_length=255, null=False, blank=True)
    portal = models.ForeignKey(Portal, null=True, blank=True,
                                                related_name="textlabels")

    main_text = models.TextField(blank=True)

    biography = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=False, default=1)


class CMSLabel(models.Model):

    date = models.CharField(max_length=255, null=False)
    text = models.TextField()
    museumobject = models.ForeignKey(MuseumObject)

    def __unicode__(self):
        return u"%s for %s" % (self.date, self.museumobject.museum_number)


class Image(models.Model):

    image_id = models.CharField(max_length=16, null=False, blank=True)
    caption = models.CharField(max_length=255, null=False, blank=True)
    image_file = ImageField(upload_to="labels/images")
    position = models.PositiveIntegerField(null=False, default=1)
    museumobject = models.ForeignKey(MuseumObject, null=True, blank=True)
    textlabel = models.ForeignKey(TextLabel, null=True, blank=True)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        if self.museumobject:
            return u"%s for MN: %s" % (self.image_id, self.museumobject.museum_number)
        elif self.textlabel:
            return u"Image for TL: %s" % (self.textlabel.title)
        else:
            return unicode(self.image_file)
    @property
    def local_filename(self):
        """Where is the file stored regardless of source"""
        if unicode(self.image_file):
            return os.path.join(settings.MEDIA_ROOT,
                                self.image_file.field.upload_to,
                                unicode(self.image_file.file))
        else:
            return None

    @property
    def local_vadar_filename(self):
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
                local_file = open(self.local_vadar_filename, "wb")
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
            self.image_file = None
            return False
        except urllib2.URLError, e:
            logging.error("URL Error: %s %s" % (e.reason, image_url))
            self.image_file = None
            return False


from django.db.models.signals import pre_save, post_save
from labels.signals import get_api_data, get_related_api_data, \
                                                        create_thumbnails

pre_save.connect(get_api_data, MuseumObject)
post_save.connect(get_related_api_data, MuseumObject)
post_save.connect(create_thumbnails, Image)
