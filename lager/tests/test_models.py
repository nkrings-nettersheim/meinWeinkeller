from datetime import date, datetime

# from django.db.models import ImageFieldFile
from django.db import models
from django.test import TestCase
from ..models import Weinkeller, Weinland, Region, Jahrgang, Geschmacksrichtung, Weinart, Rebsorte, Qualitaetsstufe, \
    Erzeuger, Wein, LagerTyp, Lager, Bestand


class WeinkellerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.weinkeller = Weinkeller.objects.create(
            weinkeller='Mein Weinkeller',
            weinkeller_admin_id=1,
            weinkeller_user_id=1
        )

    def test_model_content(self):
        self.assertEqual(self.weinkeller.weinkeller, "Mein Weinkeller")

    # has information
    def test_it_has_information_fields(self):
        self.assertIsInstance(self.weinkeller.weinkeller, str)
        self.assertIsInstance(self.weinkeller.weinkeller_admin_id, int)
        self.assertIsInstance(self.weinkeller.weinkeller_user_id, int)

    # test label
    def test_weinkeller_label(self):
        field_label = self.weinkeller._meta.get_field('weinkeller').verbose_name
        self.assertEqual(field_label, 'weinkeller')

    def test_weinkeller_admin_id_label(self):
        field_label = self.weinkeller._meta.get_field('weinkeller_admin_id').verbose_name
        self.assertEqual(field_label, 'weinkeller admin id')

    def test_weinkeller_user_id_label(self):
        field_label = self.weinkeller._meta.get_field('weinkeller_user_id').verbose_name
        self.assertEqual(field_label, 'weinkeller user id')

    # test max_length
    def test_weinkeller_max_length(self):
        max_length = self.weinkeller._meta.get_field('weinkeller').max_length
        self.assertEqual(max_length, 100)

    # test objects
    def test_weinkeller_str(self):
        expected_object_name = f'{self.weinkeller.weinkeller}'
        self.assertEqual(expected_object_name, str(self.weinkeller))


class WeinlandModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Weinland.objects.create(
            kontinent='Europa',
            land='Deutschland'
        )

    # has information
    def test_it_has_information_fields(self):
        weinland = Weinland.objects.get(id=1)
        self.assertIsInstance(weinland.kontinent, str)
        self.assertIsInstance(weinland.land, str)
        self.assertIsInstance(weinland.created_at, datetime)
        self.assertIsInstance(weinland.updated_at, datetime)

    # test label
    def test_kontinent_label(self):
        weinland = Weinland.objects.get(id=1)
        field_label = weinland._meta.get_field('kontinent').verbose_name
        self.assertEqual(field_label, 'kontinent')

    def test_land_label(self):
        weinland = Weinland.objects.get(id=1)
        field_label = weinland._meta.get_field('land').verbose_name
        self.assertEqual(field_label, 'land')

    def test_created_at_label(self):
        weinland = Weinland.objects.get(id=1)
        field_label = weinland._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        weinland = Weinland.objects.get(id=1)
        field_label = weinland._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    # test max_length
    def test_kontinent_max_length(self):
        weinland = Weinland.objects.get(id=1)
        max_length = weinland._meta.get_field('kontinent').max_length
        self.assertEqual(max_length, 50)

    def test_land_max_length(self):
        weinland = Weinland.objects.get(id=1)
        max_length = weinland._meta.get_field('land').max_length
        self.assertEqual(max_length, 50)

    # test objects
    def test_weinland_str(self):
        weinland = Weinland.objects.get(id=1)
        expected_object_name = f'{weinland.land}'
        self.assertEqual(expected_object_name, str(weinland))


class RegionModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Weinland.objects.create(
            kontinent='Europa',
            land='Deutschland'
        )
        Region.objects.create(
            region='Ahr',
            weinland_id='1'
        )

    # has information
    def test_it_has_information_fields(self):
        region = Region.objects.get(id=1)
        self.assertIsInstance(region.region, str)
        self.assertIsInstance(region.weinland, object)
        self.assertIsInstance(region.created_at, datetime)
        self.assertIsInstance(region.updated_at, datetime)

    # test label
    def test_kontinent_label(self):
        region = Region.objects.get(id=1)
        field_label = region._meta.get_field('region').verbose_name
        self.assertEqual(field_label, 'region')

    def test_land_label(self):
        region = Region.objects.get(id=1)
        field_label = region._meta.get_field('weinland').verbose_name
        self.assertEqual(field_label, 'weinland')

    def test_created_at_label(self):
        region = Region.objects.get(id=1)
        field_label = region._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        region = Region.objects.get(id=1)
        field_label = region._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    # test max_length
    def test_kontinent_max_length(self):
        region = Region.objects.get(id=1)
        max_length = region._meta.get_field('region').max_length
        self.assertEqual(max_length, 50)

    # test objects
    def test_weinland_str(self):
        region = Region.objects.get(id=1)
        expected_object_name = f'{region.region}'
        self.assertEqual(expected_object_name, str(region))


class JahrgangModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Jahrgang.objects.create(
            jahrgang='2001'
        )

    # has information
    def test_it_has_information_fields(self):
        jahrgang = Jahrgang.objects.get(id=1)
        self.assertIsInstance(jahrgang.jahrgang, str)
        self.assertIsInstance(jahrgang.created_at, datetime)
        self.assertIsInstance(jahrgang.updated_at, datetime)

    # test label
    def test_kontinent_label(self):
        jahrgang = Jahrgang.objects.get(id=1)
        field_label = jahrgang._meta.get_field('jahrgang').verbose_name
        self.assertEqual(field_label, 'jahrgang')

    def test_created_at_label(self):
        jahrgang = Jahrgang.objects.get(id=1)
        field_label = jahrgang._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        jahrgang = Jahrgang.objects.get(id=1)
        field_label = jahrgang._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    # test max_length
    def test_kontinent_max_length(self):
        jahrgang = Jahrgang.objects.get(id=1)
        max_length = jahrgang._meta.get_field('jahrgang').max_length
        self.assertEqual(max_length, 4)

    # test objects
    def test_weinland_str(self):
        jahrgang = Jahrgang.objects.get(id=1)
        expected_object_name = f'{jahrgang.jahrgang}'
        self.assertEqual(expected_object_name, str(jahrgang))


class GeschmacksrichtungModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Geschmacksrichtung.objects.create(
            geschmacksrichtung='trocken'
        )

    # has information
    def test_it_has_information_fields(self):
        geschmack = Geschmacksrichtung.objects.get(id=1)
        self.assertIsInstance(geschmack.geschmacksrichtung, str)
        self.assertIsInstance(geschmack.created_at, datetime)
        self.assertIsInstance(geschmack.updated_at, datetime)

    # test label
    def test_kontinent_label(self):
        geschmacksrichtung = Geschmacksrichtung.objects.get(id=1)
        field_label = geschmacksrichtung._meta.get_field('geschmacksrichtung').verbose_name
        self.assertEqual(field_label, 'geschmacksrichtung')

    def test_created_at_label(self):
        geschmacksrichtung = Geschmacksrichtung.objects.get(id=1)
        field_label = geschmacksrichtung._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        geschmacksrichtung = Geschmacksrichtung.objects.get(id=1)
        field_label = geschmacksrichtung._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

        # test max_length
        geschmacksrichtung = Geschmacksrichtung.objects.get(id=1)
        max_length = geschmacksrichtung._meta.get_field('geschmacksrichtung').max_length
        self.assertEqual(max_length, 20)

    # test objects
    def test_weinland_str(self):
        geschmacksrichtung = Geschmacksrichtung.objects.get(id=1)
        expected_object_name = f'{geschmacksrichtung.geschmacksrichtung}'
        self.assertEqual(expected_object_name, str(geschmacksrichtung))


class RebsorteModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Rebsorte.objects.create(
            rebsorte='Riesling'
        )

    # has information
    def test_it_has_information_fields(self):
        rebsorte = Rebsorte.objects.get(id=1)
        self.assertIsInstance(rebsorte.rebsorte, str)
        self.assertIsInstance(rebsorte.created_at, datetime)
        self.assertIsInstance(rebsorte.updated_at, datetime)

    # test label
    def test_kontinent_label(self):
        rebsorte = Rebsorte.objects.get(id=1)
        field_label = rebsorte._meta.get_field('rebsorte').verbose_name
        self.assertEqual(field_label, 'rebsorte')

    def test_created_at_label(self):
        rebsorte = Rebsorte.objects.get(id=1)
        field_label = rebsorte._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        rebsorte = Rebsorte.objects.get(id=1)
        field_label = rebsorte._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

        # test max_length
        rebsorte = Rebsorte.objects.get(id=1)
        max_length = rebsorte._meta.get_field('rebsorte').max_length
        self.assertEqual(max_length, 50)

    # test objects
    def test_weinland_str(self):
        rebsorte = Rebsorte.objects.get(id=1)
        expected_object_name = f'{rebsorte.rebsorte}'
        self.assertEqual(expected_object_name, str(rebsorte))


class WeinartModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Weinart.objects.create(
            weinart='Rotwein'
        )

    # has information
    def test_it_has_information_fields(self):
        weinart = Weinart.objects.get(id=1)
        self.assertIsInstance(weinart.weinart, str)

    # test label
    def test_kontinent_label(self):
        weinart = Weinart.objects.get(id=1)
        field_label = weinart._meta.get_field('weinart').verbose_name
        self.assertEqual(field_label, 'weinart')

    def test_created_at_label(self):
        weinart = Weinart.objects.get(id=1)
        field_label = weinart._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        weinart = Weinart.objects.get(id=1)
        field_label = weinart._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

        # test max_length
        weinart = Weinart.objects.get(id=1)
        max_length = weinart._meta.get_field('weinart').max_length
        self.assertEqual(max_length, 20)

    # test objects
    def test_weinland_str(self):
        weinart = Weinart.objects.get(id=1)
        expected_object_name = f'{weinart.weinart}'
        self.assertEqual(expected_object_name, str(weinart))


class QualitaetsstufeModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Qualitaetsstufe.objects.create(
            qualitaetsstufe='QbA'
        )

    # has information
    def test_it_has_information_fields(self):
        qualitaetsstufe = Qualitaetsstufe.objects.get(id=1)
        self.assertIsInstance(qualitaetsstufe.qualitaetsstufe, str)

    # test label
    def test_kontinent_label(self):
        qualitaetsstufe = Qualitaetsstufe.objects.get(id=1)
        field_label = qualitaetsstufe._meta.get_field('qualitaetsstufe').verbose_name
        self.assertEqual(field_label, 'qualitaetsstufe')

    def test_created_at_label(self):
        qualitaetsstufe = Qualitaetsstufe.objects.get(id=1)
        field_label = qualitaetsstufe._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        qualitaetsstufe = Qualitaetsstufe.objects.get(id=1)
        field_label = qualitaetsstufe._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

        # test max_length
        qualitaetsstufe = Qualitaetsstufe.objects.get(id=1)
        max_length = qualitaetsstufe._meta.get_field('qualitaetsstufe').max_length
        self.assertEqual(max_length, 50)

    # test objects
    def test_weinland_str(self):
        qualitaetsstufe = Qualitaetsstufe.objects.get(id=1)
        expected_object_name = f'{qualitaetsstufe.qualitaetsstufe}'
        self.assertEqual(expected_object_name, str(qualitaetsstufe))


class ErzeugerModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Weinland.objects.create(
            kontinent='Europa',
            land='Deutschland'
        )
        Erzeuger.objects.create(
            name='Franz Keller',
            inhaber='Fritz Keller'
        )

    # has information

    # test label

    # test max_length

    # test objects
    def test_erzeuger_str(self):
        erzeuger = Erzeuger.objects.get(id=1)
        expected_object_name = f'{erzeuger.name}'
        self.assertEqual(expected_object_name, str('Franz Keller'))


class WeinModelTest(TestCase):
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

    # has information
    def test_it_has_information_fields(self):
        wein = Wein.objects.get(id=1)
        self.assertIsInstance(wein.name, str)

    # test label

    # test max_length

    # test objects
    def test_wein_str(self):
        wein = Wein.objects.get(id=1)
        expected_object_name = f'{wein.name}, {wein.jahrgang}, {wein.erzeuger}'
        self.assertEqual(expected_object_name, str(wein))


class LagerTypModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        LagerTyp.objects.create(
            typ="Matrix"
        )

    # test objects
    def test_lagertyp_str(self):
        lagertyp = LagerTyp.objects.get(id=1)
        expected_object_name = f'{lagertyp.typ}'
        self.assertEqual(expected_object_name, str(lagertyp))


class LagerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        LagerTyp.objects.create(
            typ="Matrix"
        )
        Lager.objects.create(
            name="Keller",
            typ_id='1'
        )

    # test objects
    def test_lager_str(self):
        lager = Lager.objects.get(id=1)
        expected_object_name = f'{lager.name}'
        self.assertEqual(expected_object_name, str(lager))


class BestandModelTest(TestCase):
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

    # test objects
    def test_bestand_str(self):
        bestand = Bestand.objects.get(id=1)
        expected_object_name = f'{bestand.wein}'
        self.assertEqual(expected_object_name, str(bestand))

