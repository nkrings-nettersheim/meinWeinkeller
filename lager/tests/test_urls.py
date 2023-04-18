from django.test import SimpleTestCase
from django.urls import resolve, reverse
from lager.views import *


class TestUrls(SimpleTestCase):

    def test_url_index_is_resolved(self):
        url = reverse('lager:index')
        self.assertEqual(resolve(url).func, index)

    def test_url_impressum_is_resolved(self):
        url = reverse('lager:impressum')
        self.assertEqual(resolve(url).func, impressum)

    def test_url_datenschutz_is_resolved(self):
        url = reverse('lager:datenschutz')
        self.assertEqual(resolve(url).func, datenschutz)

    def test_url_add_weinland_is_resolved(self):
        url = reverse('lager:add_weinland')
        self.assertEqual(resolve(url).func, add_weinland)

    def test_url_edit_weinland_is_resolved(self):
        url = reverse('lager:edit_weinland', args=['1'])
        self.assertEqual(resolve(url).func, edit_weinland)

    #def test_url_list_weinlands_is_resolved(self):
    #    url = reverse('lager:list_weinlands')
    #    self.assertEqual(resolve(url).func, list_weinlands)

    #def test_url_delete_weinland_is_resolved(self):
    #    url = reverse('lager:delete_weinland_item', args=['1'])
    #    self.assertEqual(resolve(url).func, delete_weinland_item)

    def test_url_weinland_is_resolved(self):
        url = reverse('lager:weinland', args=['1'])
        self.assertEqual(resolve(url).func, weinland)

