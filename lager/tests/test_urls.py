from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from lager.views import *


# Tests around Homepage, Impressum Datenschutz
class HomepageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.weinkeller = Weinkeller.objects.create(
            weinkeller='Mein Weinkeller',
            weinkeller_admin_id=1,
            weinkeller_user_id=1
        )

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 301)

    def test_homepage_available_by_name(self):
        response = self.client.get(reverse('lager:index'))
        self.assertEqual(response.status_code, 302)

    def test_impressum_exists_at_correct_location(self):
        response = self.client.get("/lager/impressum/")
        self.assertEqual(response.status_code, 200)

    def test_impressum_available_by_name(self):
        response = self.client.get(reverse('lager:impressum'))
        self.assertEqual(response.status_code, 200)

    def test_datenschutz_exists_at_correct_location(self):
        response = self.client.get("/lager/datenschutz/")
        self.assertEqual(response.status_code, 200)

    def test_datenschutz_available_by_name(self):
        response = self.client.get(reverse('lager:datenschutz'))
        self.assertEqual(response.status_code, 200)

    def test_url_impressum_is_resolved(self):
        url = reverse('lager:impressum')
        self.assertEqual(resolve(url).func, impressum)

    def test_url_datenschutz_is_resolved(self):
        url = reverse('lager:datenschutz')
        self.assertEqual(resolve(url).func, datenschutz)


class WeinlandTests(TestCase):
    @classmethod
    def setUp(cls):
        Weinland.objects.create(
            kontinent='Europa',
            land='Deutschland'
        )

    # add_weinland
    def test_add_weinland_exists_at_correct_location(self):
        response = self.client.get("/lager/add/weinland/")
        self.assertEqual(response.status_code, 302)

    def test_add_weinland_available_by_name(self):
        response = self.client.get(reverse('lager:add_weinland'))
        self.assertEqual(response.status_code, 302)

    def test_url_add_weinland_is_resolved(self):
        url = reverse('lager:add_weinland')
        self.assertEqual(resolve(url).func, add_weinland)

    # edit_weinland
    def test_edit_weinland_exists_at_correct_location(self):
        response = self.client.get("/lager/edit/weinland/1")
        self.assertEqual(response.status_code, 301)

    def test_edit_weinland_available_by_name(self):
        response = self.client.get(reverse('lager:edit_weinland', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_url_edit_weinland_is_resolved(self):
        url = reverse('lager:edit_weinland', args=['1'])
        self.assertEqual(resolve(url).func, edit_weinland)

    # list_weinlands
    def test_list_weinlands_exists_at_correct_location(self):
        response = self.client.get("/lager/list/weinland/")
        self.assertEqual(response.status_code, 302)

    def test_list_weinland_available_by_name(self):
        response = self.client.get(reverse('lager:list_weinlands'))
        self.assertEqual(response.status_code, 302)
        # Funktioniert nicht, wegen der 302
        #self.assertTemplateUsed(response, "lager/weinlands.html")
        #self.assertContains(response, "<h2>Liste der Weinländer</h2>")

    # delete/weinland/<pk>

    # weinland
    def test_url_weinland_is_resolved(self):
        url = reverse('lager:weinland', args=['1'])
        self.assertEqual(resolve(url).func, weinland)
