import codecs
import os
from distutils.dir_util import copy_tree
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.test.client import Client
from django.template.defaultfilters import slugify
from labels.models import DigitalLabel, Portal


class Command(BaseCommand):

    args = "<digitallabel_id digitallabel_id>"
    help = "Creates a static bundle of HTML, media and images for the labels"
    option_list = BaseCommand.option_list + (
        make_option('-o',
            '--out',
            default=".",
            help="Where to put them?"
        ),
    )

    def handle(self, *args, **options):
        destination = options['out']

        for dl in DigitalLabel.objects.all():
            self.save_html(dl, destination)

        for pt in Portal.objects.all():
            self.save_html(pt, destination)

        # handle static media: JS, IMG, CSS, etc.

        # SOURCE DIRS
        media_abspath = os.path.abspath(settings.MEDIA_ROOT)
        static_abspath = os.path.abspath(settings.STATIC_ROOT)

        # DESTINATION DIRS
        static_build_dir = os.path.join(destination,
                                        os.path.basename(static_abspath))
        media_build_dir = os.path.join(destination,
                                       os.path.basename(media_abspath),
                                       'cache')

        # COPY FILES
        copy_tree(settings.STATIC_ROOT, static_build_dir)
        copy_tree(os.path.join(settings.MEDIA_ROOT, 'cache'), media_build_dir)

    def save_html(self, screen, destination):
        cl = Client()
        page_html = cl.get('/%s/%d/' % (screen.model_name, screen.pk)).content

        # make img, css and js links relative
        page_html = page_html.replace('data-img-l="/', 'data-img-l="./'
                            ).replace('src="/', 'src="./'
                            ).replace('href="/', 'href="./')

        dest_abspath = os.path.abspath(destination)
        if not os.path.exists(dest_abspath):
            print 'Making %s' % (dest_abspath)
            os.mkdir(dest_abspath)

        filename = os.path.join(destination,
                        '%s.html' % (slugify(screen.name)))
        f = codecs.open(filename, 'w', 'UTF-8')
        unicode_html = unicode(page_html, 'UTF-8')
        f.write(unicode_html)

