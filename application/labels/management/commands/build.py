import codecs
import os
from distutils.dir_util import copy_tree
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.test.client import Client
from labels.models import Group


class Command(BaseCommand):

    args = "<group_id group_id>"
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
        if not args:
            g_ids = [g.id for g in Group.objects.all()]
        else:
            g_ids = [int(a) for a in args]

        for gid in g_ids:
            self.save_html(gid, destination)

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

    def save_html(self, group_id, destination):
        cl = Client()
        page_html = cl.get('/group/%d/' % group_id).content

        # make img, css and js links relative
        page_html = page_html.replace('data-img-l="/', 'data-img-l="./'
                            ).replace('src="/', 'src="./'
                            ).replace('href="/', 'href="./')

        dest_abspath = os.path.abspath(destination)
        if not os.path.exists(dest_abspath):
            print 'Making %s' % (dest_abspath)
            os.mkdir(dest_abspath)

        filename = os.path.join(destination, '%d.html' % (group_id))
        f = codecs.open(filename, 'w', 'UTF-8')
        f.write(page_html)

