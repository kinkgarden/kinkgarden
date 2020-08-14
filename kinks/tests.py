import typing

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from .models import Kink, KinkList, KinkListColumn, ConcreteKink
from base.tests import approve_age_gate


def make_test_data(list_args: typing.Optional[dict] = None):
    if list_args is None:
        list_args = {}
    standard_kink_name = 'Sample Standard'
    standard_kink_description = 'This is a sample standard kink.'
    standard_kink = Kink.objects.create(name=standard_kink_name, description=standard_kink_description,
                                        category=None)
    custom_kink_name = 'Sample Custom'
    custom_kink_description = 'This is a sample custom kink.'
    kink_list = KinkList.objects.create(**list_args)
    kink_list.standardkinklistentry_set.create(column=KinkListColumn.HEART.value, kink=standard_kink)
    kink_list.customkinklistentry_set.create(column=KinkListColumn.NO.value, custom_name=custom_kink_name,
                                             custom_description=custom_kink_description)
    return custom_kink_description, custom_kink_name, kink_list, standard_kink_description, standard_kink_name


class KinkListModelTests(TestCase):
    def test_columns_retrieves_both_standard_and_custom(self):
        custom_description, custom_name, kink_list, standard_description, standard_name = make_test_data()

        actual_columns = kink_list.columns
        self.assertEqual(actual_columns[0][0], 'heart')
        self.assertListEqual(actual_columns[0][1], [ConcreteKink(standard_name, standard_description)])
        self.assertEqual(actual_columns[1][0], 'check')
        self.assertListEqual(actual_columns[1][1], [])
        self.assertEqual(actual_columns[2][0], 'tilde')
        self.assertListEqual(actual_columns[2][1], [])
        self.assertEqual(actual_columns[3][0], 'no')
        self.assertListEqual(actual_columns[3][1], [ConcreteKink(custom_name, custom_description)])


class KinkListViewTests(TestCase):
    def setUp(self):
        approve_age_gate(self.client)

    def test_list_without_password_shows_correctly(self):
        custom_description, custom_name, kink_list, standard_description, standard_name = make_test_data()

        response = self.client.get(kink_list.get_absolute_url())
        self.assertContains(response, standard_name)
        self.assertContains(response, custom_name)

    def test_list_with_password_is_private(self):
        view_password = 'insecure'
        list_args = dict(view_password=make_password(view_password))
        custom_description, custom_name, kink_list, standard_description, standard_name = make_test_data(list_args)

        response = self.client.get(kink_list.get_absolute_url())
        self.assertContains(response, '<input type="password" name="view-password">', status_code=403, html=True)
        response = self.client.post(kink_list.get_absolute_url(), {'view-password': view_password})
        self.assertContains(response, standard_name)
        self.assertContains(response, custom_name)
