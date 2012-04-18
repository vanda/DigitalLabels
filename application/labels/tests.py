"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from labels.models import CMSLabel, DigitalLabel


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class LabelTest(TestCase):

        def test_label_download(self):
            dl = DigitalLabel.objects.get_or_create(object_number='O9138')
            print 'foo'
