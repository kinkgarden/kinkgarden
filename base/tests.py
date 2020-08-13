from django.test import TestCase


class RTAMiddlewareTests(TestCase):
    def test_index_has_rta_header(self):
        response = self.client.get('/')
        self.assertEqual(response['Rating'], 'RTA-5042-1996-1400-1577-RTA')
