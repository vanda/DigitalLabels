from django.core.management.base import BaseCommand
from labels.models import Image

class Command(BaseCommand):

    args = ""
    help = "Ensures image variations available for display/thumbnails."

    def handle(self, *args, **options):
        c = 0
        for i in Image.objects.all():
            c+=1
            print c, i
            i.save()
