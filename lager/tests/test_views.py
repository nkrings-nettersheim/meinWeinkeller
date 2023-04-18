import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..models import Geschmacksrichtung, Weinart, Weinland, Region, Rebsorte, Jahrgang, Erzeuger, Wein, Weinkeller, \
    LagerTyp, Lager, Bestand


# from ..models import Album

# TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')

# class ViewsTestCase(TestCase):
#    def test_index_loads_properly(self):
#        response = self.client.get('')
#        self.assertEqual(response.status_code, 301)#

#    def test_lager_loads_properly(self):
#        response = self.client.get('/lager/')
#        self.assertEqual(response.status_code, 200)

class LagerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Geschmacksrichtung.objects.create(
            geschmacksrichtung='trocken'
        )
        Weinart.objects.create(
            weinart='Weißwein'
        )
        Weinland.objects.create(
            kontinent='Europa',
            land='Deutschland'
        )
        Rebsorte.objects.create(
            rebsorte='Riesling'
        )
        Jahrgang.objects.create(
            jahrgang='2001'
        )
        Erzeuger.objects.create(
            name='Franz Keller',
            inhaber='Fritz Keller'
        )
        Wein.objects.create(
            name='Oberbergener Baßgeige',
            weinland_id='1',
            rebsorte_id='1',
            weinart_id='1',
            jahrgang_id='1',
            geschmacksrichtung_id='1',
            erzeuger_id='1',
            literpreis='12.80',
            preis='10.80'
        )
        LagerTyp.objects.create(
            typ="Matrix"
        )
        Lager.objects.create(
            name="Keller",
            typ_id='1'
        )

        Bestand.objects.create(
            wein_id="1",
            lager_id='1'
        )

    def test_impressum(self):
        response = self.client.get(reverse("lager:impressum"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lager/impressum.html")
        self.assertContains(response, "Impressum")
        self.assertContains(response, 'Mein Weinkeller - Impressum')  # Title

    def test_datenschutz(self):
        response = self.client.get(reverse("lager:datenschutz"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lager/datenschutz.html")
        self.assertContains(response, "Datenschutz")
        self.assertContains(response, 'Mein Weinkeller - Datenschutz')  # Title
