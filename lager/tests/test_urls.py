from django.test import SimpleTestCase
from django.urls import resolve, reverse
from lager.views import index, impressum, datenschutz


class TestUrls(SimpleTestCase):

#    def test_url_index_is_resolved(self):
#        url = reverse('lager:index')
#        print(url)
#        self.assertEqual(resolve(url).func, index)

    def test_url_impressum_is_resolved(self):
        url = reverse('lager:impressum')
        self.assertEqual(resolve(url).func, impressum)

    def test_url_datenschutz_is_resolved(self):
        url = reverse('lager:datenschutz')
        self.assertEqual(resolve(url).func, datenschutz)
