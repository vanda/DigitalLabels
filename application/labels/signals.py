import urllib2
from django.utils import simplejson
from django.conf import settings
from labels.models import CMSLabel

def get_api_data(sender, instance, **kwargs):

    if instance.id == None or instance.redownload == True:
        item_url = 'http://%s/api/json/museumobject/%s/' % (
                                    settings.COLLECTIONS_API_HOSTNAME,
                                    instance.object_number)
        try:
            response = urllib2.urlopen(item_url)
            museum_object = simplejson.load(response)[0]

            label_name = ''
            object_name = museum_object['fields']['object']
            object_title = museum_object['fields']['title']

            if (object_name and object_title) and (object_name !=
                                                        object_title):
                label_name = "%s (%s)" % (object_title, object_name)
            else:
                label_name = object_name

            instance.name = label_name
            instance.museum_number = museum_object['fields']['museum_number']
            instance.materials_techniques = \
                            museum_object['fields']['materials_techniques']

            instance.artist_maker = museum_object['fields']['artist']
            instance.date_text = museum_object['fields']['date_text']
            instance.credit_line = museum_object['fields']['credit']

        except urllib2.HTTPError, e:
            if e.code == 404:
                # Missing object
                pass
            else:
                # other HTTP error
                pass

            # record error in title
            instance.name = "* UNABLE TO GET RECORD DATA FOR %s *" % (
                                                    instance.object_number)

        # don't redownload again
        instance.redownload = False

        # prepare to redownload labels in post save
        instance.cmslabel_set.all().delete()

def get_cms_labels(sender, instance, **kwargs):
    """
    Retrieve current data from the API and use to populate label
    """

    if instance.cmslabel_set.count() == 0:
        item_url = 'http://%s/api/json/museumobject/%s/' % (
                                    settings.COLLECTIONS_API_HOSTNAME,
                                    instance.object_number)
        try:
            response = urllib2.urlopen(item_url)
            museum_object = simplejson.load(response)[0]
            for l in museum_object['fields']['labels']:

                cms_label = CMSLabel()
                cms_label.date = l['fields']['date']
                cms_label.text = l['fields']['label_text']
                cms_label.digitallabel = instance
                cms_label.save()

        except urllib2.HTTPError, e:
            if e.code == 404:
                # Missing object
                pass
            else:
                # other error
                pass




