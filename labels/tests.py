"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from labels.models import MuseumObject, DigitalLabel, Portal, TextLabel, Image


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ObjectTest(TestCase):

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

    def test_new_loanobject(self):
        """
        Loan objects do not have O numbers but don't punish them
        """
        mo = MuseumObject()
        mo.name = 'Name'
        mo.date_text = 'Date text'
        mo.artist_maker = 'Artist maker'
        mo.place = 'Place'
        mo.materials_techniques = 'Materials techniques'
        mo.museum_number = 'Museum number'
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


class DLabelTest(TestCase):

    def setUp(self):
        #create a portal
        dl = DigitalLabel()
        dl.name = 'Turning'
        dl.save()

    def test_label_object(self):
        mo = MuseumObject()
        mo.object_number = 'O73708'
        mo.digitallabel = DigitalLabel.objects.get(id=1)
        mo.save()

        response = self.client.get('/digitallabel/1/')
        self.assertContains(response, '<div class="title"><h2>Washstand</h2></div>', 1, 200)

    def test_gateway_object(self):
        mo = MuseumObject()
        mo.object_number = 'O59319'
        mo.digitallabel = DigitalLabel.objects.get(id=1)
        mo.gateway_object = True
        mo.save()

        response = self.client.get('/digitallabel/1/')
        self.assertContains(response, """<li class="home txt obj">
                <div class="mask"></div>
                <div class="title"><h2>Armchair</h2></div>""", 1, 200)

    def test_timeout_images(self):
        mo = MuseumObject()
        mo.object_number = 'O321535'
        mo.digitallabel = DigitalLabel.objects.get(id=1)
        mo.save()

        response = self.client.get('/digitallabel/1/')
        self.assertNotContains(response, '<img class="timeout"', 200)

        dl = DigitalLabel.objects.get(id=1)
        dl.timeout_images.add(Image.objects.get(id=1))

        response = self.client.get('/digitallabel/1/')
        self.assertContains(response, '<img class="timeout"', 1, 200)


class PortalTest(TestCase):

    def setUp(self):
        #create a portal
        pt = Portal()
        pt.name = 'Frank Lloyd Wright'
        pt.save()

    def test_textlabel(self):
        #create a Text Label
        tl = TextLabel()
        tl.title = 'Frank Lloyd Wright (Biography)'
        tl.portal_id = 1
        tl.biography = True
        tl.main_text = """Frank Lloyd Wright (born Frank Lincoln Wright,
                            June 8, 1867 - April 9, 1959) was an American architect,
                            interior designer, writer and educator, who designed
                            more than 1,000 structures and completed 500 works.
                            Wright believed in designing structures which were
                            in harmony with humanity and its environment, a
                            philosophy he called organic architecture. This
                            philosophy was best exemplified by his design for
                            Fallingwater (1935), which has been called "the best
                            all-time work of American architecture".[1] Wright was
                            a leader of the Prairie School movement of architecture
                            and developed the concept of the Usonian home, his unique
                            vision for urban planning in the United States."""
        tl.save()

        #test the text label appear in the HTML of the portal page
        response = self.client.get('/portal/1/')
        self.assertContains(response, """<div class="title"><h2>Frank Lloyd Wright (Biography)</h2></div>""", 1, 200)

    def test_museumobject(self):
        #create a Museum Object
        mo = MuseumObject()
        mo.name = 'Armchair'
        mo.portal = Portal.objects.get(id=1)
        mo.date_text = '1904 (made)'
        mo.artist_maker = 'Wright, Frank Lloyd'
        mo.place = 'America'
        mo.materials_techniques = """Frame: painted steel, with cast-iron base and rubber
                                        castersUpholstery: slip seat with horsehair(?)
                                        stuffing, and leather cover (probably original)"""
        mo.museum_number = 'W.43-1981'
        mo.object_number = 'O112088'
        mo.credit_line = 'Lorem ipsum'
        mo.main_text = """Wright designed a variety of metal chairs and desks for the
                            headquarters of this mail-order soap company. The client's
                            requirement that the building be fireproof provided the
                            impetus for Wright's use of metal. The form of the chair
                            and the decoration of perforated squares on the back indicate
                            Wright's likely awareness of contemporary Viennese design."""
        mo.save()

        #test the object appear in the Portal
        response = self.client.get('/portal/1/')
        self.assertContains(response, '<div class="title"><h2>Armchair</h2></div>', 1, 200)

    def test_edit_TextLabel(self):
        #create a new Text Label
        tl = TextLabel()
        tl.title = 'Historical Context 2'
        tl.portal = Portal.objects.get(id=1)
        tl.biography = False
        tl.main_text = """The massive stained oak table combines forms derived from the
                            Gothic Revival and Arts and Crafts movements of the later
                            19th century. The colour and shape of the table, and of other
                            pieces of furniture, were echoed in interior details throughout
                            the house. Wright believed that wood should be cut simply and
                            stained (never varnished) to reveal the 'nature' of the material."""
        tl.save()

        #get the Text Label and set the new title 
        tl = TextLabel.objects.get(id=1)
        replacing_title = 'The stained oak table'
        self.assertNotEqual(tl.title, replacing_title)

        # change the title
        tl.title = replacing_title
        tl.save()
        self.assertEqual(tl.title, replacing_title)

        #test the title has changed in the portal view
        response = self.client.get('/portal/1/')
        self.assertContains(response, """<div class="title"><h2>The stained oak table</h2></div>""", 1, 200)
