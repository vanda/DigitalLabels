import os, shutil
from django.core.management.base import NoArgsCommand
from django.db import connection, transaction
from labels.models import Image


class Command(NoArgsCommand):
    """
    This scrpt complete the migration job previously done by removing the museum object images duplicates
    It will then re-create the thumbnails for all the existing images 
    """

    def handle_noargs(self, **options):
        cursor = connection.cursor()

        os.remove('labelsite/media/labels/images/Dummy_25.jpg')
        os.remove('labelsite/media/labels/images/2012FE9004.jpg')
        os.remove('labelsite/media/labels/images/2012FE9003.jpg')
        os.remove('labelsite/media/labels/images/content.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8620.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8619.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8618.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8617.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8616.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8615.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8614.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8613.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8612.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8611.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8610.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8609.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8608.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8607.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8606.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8605.jpg')
        os.remove('labelsite/media/labels/images/2006AJ8604.jpg')
        os.remove('labelsite/media/labels/images/2006AT2425.jpg')
        os.remove('labelsite/media/labels/images/2006AP8063.jpg')
        os.remove('labelsite/media/labels/images/2006AU2831_1.jpg')
        os.remove('labelsite/media/labels/images/img060_1.jpg')
        os.remove('labelsite/media/labels/images/img058.jpg')
        os.remove('labelsite/media/labels/images/2006AU1797_1.jpg')
        os.remove('labelsite/media/labels/images/2012FN4909.jpg')
        os.remove('labelsite/media/labels/images/Dummy_110.jpg')
        os.remove('labelsite/media/labels/images/2011EY5072.jpg')
        os.remove('labelsite/media/labels/images/2006AW4020.jpg')
        os.remove('labelsite/media/labels/images/Dummy_113.jpg')
        os.remove('labelsite/media/labels/images/Dummy_115.jpg')
        os.remove('labelsite/media/labels/images/2006AU4430_2.jpg')
        os.remove('labelsite/media/labels/images/2713796396_d7ac9154dc_b_1.jpg')
        os.remove('labelsite/media/labels/images/Dummy_112.jpg')
        os.remove('labelsite/media/labels/images/Dummy_116.jpg')
        os.remove('labelsite/media/labels/images/2012FP3700.jpg')
        os.remove('labelsite/media/labels/images/Dummy_117.jpg')
        os.remove('labelsite/media/labels/images/Dummy_430.jpg')

        # handling the thumbnails re-creation
        cursor.execute('DROP TABLE "thumbnail_kvstore";')
        cursor.execute("""CREATE TABLE "thumbnail_kvstore" (
            "key" varchar(200) NOT NULL PRIMARY KEY,
            "value" text NOT NULL
        );""")
        transaction.commit_unless_managed()
        shutil.rmtree('labelsite/media/cache/')
        os.makedirs('labelsite/media/cache/')
        print "Starting the thumbnail creation..."
        for i in Image.objects.all():
            i.save()
        print "Thumbnails correctly created"
