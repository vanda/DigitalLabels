import csv
import urllib
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import simplejson
from labels.models import MuseumObject, DigitalLabel, Portal, DigitalLabelObject, PortalObject

RECORDS = "O77488 O9253 O79056 O52823 O79053 O73631 O78977 O34066 O11451"


class Command(BaseCommand):

    args = "<identifier identifier>"
    help = "Preloads the database with the specified objects"

    def handle(self, *args, **options):
        dls = {}
        identifiers = []
        if not args:
            chip_grp, cr = DigitalLabel.objects.get_or_create(
                                                        name="Chippendale")
            identifiers = RECORDS.split(' ')

            # load up label hash
            for i in identifiers:
                dls[i] = chip_grp

        elif len(args) == 1 and args[0].endswith('csv'):
            reader = csv.reader(open(args[0]))
            for row in reader:
                dl_name = row[0]
                dl_no = row[2]
                mus_no = row[1]

                if dl_name.lower().find('portal') > -1:
                    pl, cr = Portal.objects.get_or_create(
                                                name=dl_no + ' ' + dl_name)
                    dls[mus_no] = pl
                else:
                    dl, cr = DigitalLabel.objects.get_or_create(
                                                name=dl_no + ' ' + dl_name)
                    dls[mus_no] = dl
                identifiers.append(mus_no)

        else:
            chip_grp = None
            identifiers = args
            for i in identifiers:
                dls[i] = None

        for identifier in identifiers:

            if identifier.startswith('O'):
                object_number = identifier
            else:
                # this is a museum number, exchange for O number
                object_number = self.get_object_by_mn(identifier)

            if object_number:
                print 'Downloading', object_number, identifier
                mo, cr = MuseumObject.objects.get_or_create(
                                            object_number=object_number)
                dl = dls[identifier]
                if dl:
                    # create the relation to the Digital Label or the Portal
                    if dl._meta.object_name == 'DigitalLabel':
                        rel = DigitalLabelObject(museumobject=mo, digitallabel=dl)
                    else:
                        rel = PortalObject(museumobject=mo, portal=dl)

                    # save the relation
                    rel.save()

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
