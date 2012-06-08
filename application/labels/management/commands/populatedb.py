import urllib
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import simplejson
from labels.models import MuseumObject, DigitalLabel

RECORDS = "O77488 O9253 O79056 O52823 O79053 O73631 O78977 O34066 O11451"


class Command(BaseCommand):

    args = "<identifier identifier>"
    help = "Preloads the database with the specified objects"

    def handle(self, *args, **options):

        if not args:
            chip_grp, cr = DigitalLabel.objects.get_or_create(
                                                        name="Chippendale")
            identifiers = RECORDS.split(' ')

        else:
            chip_grp = None
            identifiers = args

        for identifier in identifiers:

            if identifier.startswith('O'):
                object_number = identifier
            else:
                # this is a museum number, exchange for O number
                object_number = self.get_object_by_mn(identifier)

            if object_number:
                print 'Downloading', object_number
                mo, cr = MuseumObject.objects.get_or_create(
                                            object_number=object_number)
                if chip_grp:
                    mo.digitallabel = chip_grp

                mo.save()
            else:
                print 'Unable to find "O" number for %s' % (identifier)

    def get_object_by_mn(self, museum_number):
            get_params = {'mnsearch': museum_number}
            search_url = 'http://%s/api/json/museumobject/search?%s' % (
                                        settings.COLLECTIONS_API_HOSTNAME,
                                        urllib.urlencode(get_params)
                                    )
            response = urllib.urlopen(search_url)
            records = simplejson.load(response)['records']
            if len(records) == 1:
                return records[0]['fields']['object_number']
            else:
                return None
