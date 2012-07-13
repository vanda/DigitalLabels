"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from labels.models import MuseumObject


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class LabelTest(TestCase):

    def setUp(self):
        """
        Tests that we can create a copy of the API data in the
        MuseumObject model
        """
        mo, cr = MuseumObject.objects.get_or_create(object_number='O7351')

    def test_label_download(self):

        # get our label
        mo = MuseumObject.objects.get(id=1)

        # test the data fields
        self.assertTrue(len(mo.name) > 0)
        self.assertTrue(len(mo.museum_number) > 0)
        self.assertTrue(len(mo.artist_maker) > 0)

        # test the labels
        self.assertTrue(mo.cmslabel_set.count() > 0)

    def test_missing_object(self):
        mo, cr = MuseumObject.objects.get_or_create(object_number='OMISSING')

        self.assertTrue(mo.name.find('UNABLE') > -1)
        # test the labels
        self.assertTrue(mo.cmslabel_set.count() == 0)

    def test_thumbnail_url(self):

        # get our label
        mo = MuseumObject.objects.get(id=1)
        self.assertTrue(mo.thumbnail_url.endswith('jpg'))
        self.assertTrue(mo.thumbnail_tag().find('cache') > -1)

    def test_redownload(self):

        # get our label
        mo = MuseumObject.objects.get(id=1)
        original_name = mo.name
        replaced_name = 'Foo Bar Baz'
        self.assertNotEqual(mo.name, replaced_name)

        # change the name
        mo.name = replaced_name
        mo.save()
        self.assertEqual(mo.name, replaced_name)

        mo.redownload = True
        mo.save()

        # ensure original name was redownloaded
        self.assertEqual(mo.name, original_name)
        self.assertFalse(mo.redownload)

    def test_download_image(self):

        # count image
        mo = MuseumObject.objects.get(id=1)

        ims = mo.image_set.all()
        ic = ims.count()
        self.assertTrue(ic > 0)

        test_image = ims[0]

        self.assertEquals(
            unicode(test_image.image_file).find(test_image.image_id), 14)

        # check primary image position
        self.assertEquals(mo.image_set.filter(position=0).count(), 1)
        self.assertTrue(mo.image_set.filter(position=1).count() > 0)

    def test_new_object(self):

        mo = MuseumObject()
        mo.name = 'Name'
        mo.date_text = 'Date text'
        mo.artist_maker = 'Artist maker'
        mo.place = 'Place'
        mo.materials_techniques = 'Materials techniques'
        mo.museum_number = 'Museum number'
        mo.object_number = '012345'
        mo.credit_line = 'Credit line'
        mo.main_text = """Main text, main text, main text, main text,
                            main text, main text, main text, main text,
                            main text, main text, main text, main text,
                            main text, main text, main text, main text,
                            main text, main text, main text, main text,
                            main text, main text, main text, main text,
                            main text, main text, main text, main text,
                            main text, main text, main text, main text."""
        mo.save()
