from django.test import TestCase

from .models import Kink, KinkList, KinkListColumn, StandardKinkListEntry, CustomKinkListEntry, ConcreteKink


class KinkListModelTests(TestCase):
    def test_columns_retrieves_both_standard_and_custom(self):
        standard_kink_name = 'Sample Standard'
        standard_kink_description = 'This is a sample standard kink.'
        standard_kink = Kink.objects.create(name=standard_kink_name, description=standard_kink_description, category=None)
        custom_kink_name = 'Sample Custom'
        custom_kink_description = 'This is a sample custom kink.'
        kink_list = KinkList.objects.create()
        kink_list.standardkinklistentry_set.create(column=KinkListColumn.HEART.value, kink=standard_kink)
        kink_list.customkinklistentry_set.create(column=KinkListColumn.NO.value, custom_name=custom_kink_name, custom_description=custom_kink_description)

        actual_columns = kink_list.columns
        self.assertEqual(actual_columns[0][0], 'heart')
        self.assertListEqual(actual_columns[0][1], [ConcreteKink(standard_kink_name, standard_kink_description)])
        self.assertEqual(actual_columns[1][0], 'check')
        self.assertListEqual(actual_columns[1][1], [])
        self.assertEqual(actual_columns[2][0], 'tilde')
        self.assertListEqual(actual_columns[2][1], [])
        self.assertEqual(actual_columns[3][0], 'no')
        self.assertListEqual(actual_columns[3][1], [ConcreteKink(custom_kink_name, custom_kink_description)])
