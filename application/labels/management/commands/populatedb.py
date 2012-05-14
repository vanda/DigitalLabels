from django.core.management.base import BaseCommand
from labels.models import MuseumObject, DigitalLabel

RECORDS = "O77488 O9253 O79056 O52823 O79053 O73631 O78977 O34066 O11451"


class Command(BaseCommand):

    args = "<object_number object_number>"
    help = "Preloads the database with the specified objects"

    def handle(self, *args, **options):

        if not args:
            chip_grp, cr = DigitalLabel.objects.get_or_create(
                                                        name="Chippendale")
            object_nums = RECORDS.split(' ')

        else:
            chip_grp = None
            object_nums = args

        for object_number in object_nums:
            print 'Downloading', object_number
            dl, cr = MuseumObject.objects.get_or_create(
                                        object_number=object_number)
            if chip_grp:
                dl.digitallabel = chip_grp

            dl.save()
