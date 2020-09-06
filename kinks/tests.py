import typing
import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

from .models import Kink, KinkList, KinkListColumn, ConcreteKink
from base.tests import approve_age_gate


def make_standard_kink():
    standard_kink_name = "Sample Standard"
    standard_kink_description = "This is a sample standard kink."
    standard_kink = Kink.objects.create(
        name=standard_kink_name, description=standard_kink_description, category=None
    )
    return standard_kink, standard_kink_description, standard_kink_name


def make_custom_kink():
    custom_kink_name = "Sample Custom"
    custom_kink_description = "This is a sample custom kink."
    return custom_kink_description, custom_kink_name


def make_test_data(list_args: typing.Optional[dict] = None):
    if list_args is None:
        list_args = {}
    standard_kink, standard_kink_description, standard_kink_name = make_standard_kink()
    custom_kink_description, custom_kink_name = make_custom_kink()
    kink_list = KinkList.objects.create(**list_args)
    kink_list.standardkinklistentry_set.create(
        column=KinkListColumn.HEART.value, kink=standard_kink
    )
    kink_list.customkinklistentry_set.create(
        column=KinkListColumn.NO.value,
        custom_name=custom_kink_name,
        custom_description=custom_kink_description,
    )
    return (
        custom_kink_description,
        custom_kink_name,
        kink_list,
        standard_kink_description,
        standard_kink_name,
    )


class KinkListModelTests(TestCase):
    def test_columns_retrieves_both_standard_and_custom(self):
        (
            custom_description,
            custom_name,
            kink_list,
            standard_description,
            standard_name,
        ) = make_test_data()

        actual_columns = kink_list.columns
        self.assertEqual(actual_columns[0][0], "heart")
        self.assertListEqual(
            actual_columns[0][1], [ConcreteKink(standard_name, standard_description)]
        )
        self.assertEqual(actual_columns[1][0], "check")
        self.assertListEqual(actual_columns[1][1], [])
        self.assertEqual(actual_columns[2][0], "tilde")
        self.assertListEqual(actual_columns[2][1], [])
        self.assertEqual(actual_columns[3][0], "no")
        self.assertListEqual(
            actual_columns[3][1], [ConcreteKink(custom_name, custom_description)]
        )


class KinkListViewTests(TestCase):
    def setUp(self):
        approve_age_gate(self.client)

    def test_list_without_password_shows_correctly(self):
        (
            custom_description,
            custom_name,
            kink_list,
            standard_description,
            standard_name,
        ) = make_test_data()

        response = self.client.get(kink_list.get_absolute_url())
        self.assertContains(response, standard_name)
        self.assertContains(response, custom_name)

    def test_list_with_password_is_private(self):
        view_password = "insecure"
        list_args = dict(view_password=make_password(view_password))
        (
            custom_description,
            custom_name,
            kink_list,
            standard_description,
            standard_name,
        ) = make_test_data(list_args)

        response = self.client.get(kink_list.get_absolute_url())
        self.assertContains(
            response,
            '<input type="password" name="view-password">',
            status_code=403,
            html=True,
        )
        response = self.client.post(
            kink_list.get_absolute_url(), {"view-password": "the-wrong-thing"}
        )
        self.assertContains(
            response,
            '<input type="password" name="view-password">',
            status_code=403,
            html=True,
        )
        self.assertContains(response, "Incorrect password", status_code=403)
        response = self.client.post(
            kink_list.get_absolute_url(), {"view-password": view_password}
        )
        self.assertContains(response, standard_name)
        self.assertContains(response, custom_name)

    def test_nonexistent_list_deniable(self):
        import uuid

        fake_uuid = uuid.uuid4()
        path = reverse("kinks:kink_list", args=(fake_uuid,))
        response = self.client.get(path)
        self.assertContains(
            response,
            '<input type="password" name="view-password">',
            status_code=403,
            html=True,
        )
        response = self.client.post(path, {"view-password": "anything"})
        self.assertContains(
            response,
            '<input type="password" name="view-password">',
            status_code=403,
            html=True,
        )
        self.assertContains(response, "Incorrect password", status_code=403)

    def test_admin_delete_flag_hides_custom(self):
        (
            custom_description,
            custom_name,
            kink_list,
            standard_description,
            standard_name,
        ) = make_test_data()

        custom = kink_list.customkinklistentry_set.get()
        custom.admin_delete = True
        custom.save()

        response = self.client.get(kink_list.get_absolute_url())
        self.assertContains(response, standard_name)
        self.assertNotContains(response, custom_name)


class KinkListCreateTests(TestCase):
    def setUp(self):
        approve_age_gate(self.client)

    def test_create_list_works(self):
        standard_kink, standard_description, standard_name = make_standard_kink()
        custom_description, custom_name = make_custom_kink()
        response = self.client.post(
            reverse("kinks:kink_list_new"),
            {
                "view-password": "",
                "edit-password": "",
                "kink-list-data": json.dumps(
                    [
                        {
                            "name": "heart",
                            "kinks": [{"custom": False, "id": standard_kink.id}],
                        },
                        {"name": "check", "kinks": []},
                        {"name": "tilde", "kinks": []},
                        {
                            "name": "no",
                            "kinks": [
                                {
                                    "custom": True,
                                    "name": custom_name,
                                    "description": custom_description,
                                }
                            ],
                        },
                    ]
                ),
            },
        )
        kink_list = KinkList.objects.get()
        self.assertRedirects(response, kink_list.get_absolute_url())

        response = self.client.get(kink_list.get_absolute_url())
        self.assertContains(response, standard_name)
        self.assertContains(response, custom_name)

    def test_create_list_passwords_work(self):
        view_password = "insecure"
        edit_password = "also_insecure"
        response = self.client.post(
            reverse("kinks:kink_list_new"),
            {
                "view-password": view_password,
                "edit-password": edit_password,
                "kink-list-data": json.dumps(
                    [
                        {"name": "heart", "kinks": []},
                        {"name": "check", "kinks": []},
                        {"name": "tilde", "kinks": []},
                        {"name": "no", "kinks": []},
                    ]
                ),
            },
        )
        kink_list = KinkList.objects.get()
        self.assertRedirects(
            response, kink_list.get_absolute_url(), target_status_code=403
        )

        self.assertTrue(check_password(view_password, kink_list.view_password))
        self.assertTrue(check_password(edit_password, kink_list.edit_password))


class KinkListEditTests(TestCase):
    def setUp(self):
        approve_age_gate(self.client)

    def test_edit_happy_path_works(self):
        edit_password = "insecure"
        list_args = dict(edit_password=make_password(edit_password))
        (
            custom_description,
            custom_name,
            kink_list,
            standard_description,
            standard_name,
        ) = make_test_data(list_args)

        old_standard_kink = Kink.objects.get()
        new_standard_kink = Kink.objects.create(
            name="another standard kink", description=""
        )
        kink_list.standardkinklistentry_set.create(
            kink=new_standard_kink, column=KinkListColumn.CHECK.value
        )
        kink_list.customkinklistentry_set.create(
            custom_name=custom_name + " 2",
            custom_description="",
            column=KinkListColumn.TILDE.value,
        )

        edit_url = reverse("kinks:kink_list_edit", args=(kink_list.id,))
        response = self.client.get(edit_url)
        self.assertContains(
            response,
            '<input type="password" name="edit-password">',
            status_code=403,
            html=True,
        )
        response = self.client.post(edit_url, {"edit-password": "the-wrong-thing"})
        self.assertContains(
            response,
            '<input type="password" name="edit-password">',
            status_code=403,
            html=True,
        )
        self.assertContains(response, "Incorrect password", status_code=403)
        response = self.client.post(edit_url, {"edit-password": edit_password})
        self.assertTemplateUsed(response, "editor/editor.html")

        newer_standard_kink = Kink.objects.create(
            name="one more standard kink", description=""
        )

        response = self.client.post(
            reverse("kinks:kink_list_save", args=(kink_list.id,)),
            {
                "view-password": "",
                "edit-password": "",
                "kink-list-data": json.dumps(
                    [
                        {
                            "name": "heart",
                            "kinks": [{"custom": False, "id": newer_standard_kink.id}],
                        },
                        {
                            "name": "check",
                            "kinks": [{"custom": False, "id": old_standard_kink.id}],
                        },
                        {
                            "name": "tilde",
                            "kinks": [
                                {
                                    "custom": True,
                                    "name": custom_name,
                                    "description": custom_description,
                                }
                            ],
                        },
                        {
                            "name": "no",
                            "kinks": [
                                {
                                    "custom": True,
                                    "name": custom_name + " 3",
                                    "description": custom_description,
                                }
                            ],
                        },
                    ]
                ),
            },
        )
        self.assertRedirects(response, kink_list.get_absolute_url())

        actual_columns = kink_list.columns
        self.assertEqual(actual_columns[0][0], "heart")
        self.assertListEqual(
            actual_columns[0][1],
            [ConcreteKink(newer_standard_kink.name, newer_standard_kink.description)],
        )
        self.assertEqual(actual_columns[1][0], "check")
        self.assertListEqual(
            actual_columns[1][1], [ConcreteKink(standard_name, standard_description)]
        )
        self.assertEqual(actual_columns[2][0], "tilde")
        self.assertListEqual(
            actual_columns[2][1], [ConcreteKink(custom_name, custom_description)]
        )
        self.assertEqual(actual_columns[3][0], "no")
        self.assertListEqual(
            actual_columns[3][1], [ConcreteKink(custom_name + " 3", custom_description)]
        )

    def test_nonexistent_list_deniable(self):
        import uuid

        fake_uuid = uuid.uuid4()
        path = reverse("kinks:kink_list_edit", args=(fake_uuid,))
        response = self.client.get(path)
        self.assertContains(
            response,
            '<input type="password" name="edit-password">',
            status_code=403,
            html=True,
        )
        response = self.client.post(path, {"edit-password": "anything"})
        self.assertContains(
            response,
            '<input type="password" name="edit-password">',
            status_code=403,
            html=True,
        )
        self.assertContains(response, "Incorrect password", status_code=403)

    def test_list_save_dishonesty_prevention(self):
        (
            custom_description,
            custom_name,
            target,
            standard_description,
            standard_name,
        ) = make_test_data()

        gate_edit_password = "insecure"
        gate = KinkList.objects.create(edit_password=gate_edit_password)

        self.client.post(
            reverse("kinks:kink_list_edit", args=(gate.id,)),
            {"edit-password": gate_edit_password},
        )

        response = self.client.post(
            reverse("kinks:kink_list_save", args=(target.id,)),
            {
                "view-password": "",
                "edit-password": "",
                "kink-list-data": json.dumps(
                    [
                        {"name": "heart", "kinks": []},
                        {"name": "check", "kinks": []},
                        {"name": "tilde", "kinks": []},
                        {"name": "no", "kinks": []},
                    ]
                ),
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(target.standardkinklistentry_set.count(), 1)

    def test_multi_list_drifting(self):
        edit_password = "insecure"
        list_args = dict(edit_password=make_password(edit_password))
        (
            custom_description,
            custom_name,
            kink_list1,
            standard_description,
            standard_name,
        ) = make_test_data(list_args)
        kink_list2 = KinkList.objects.create(**list_args)

        self.client.post(
            reverse("kinks:kink_list_edit", args=(kink_list1.id,)),
            {"edit-password": edit_password},
        )
        self.client.post(
            reverse("kinks:kink_list_edit", args=(kink_list2.id,)),
            {"edit-password": edit_password},
        )

        editor_data = {
            "view-password": "",
            "edit-password": "",
            "kink-list-data": json.dumps(
                [
                    {"name": "heart", "kinks": []},
                    {"name": "check", "kinks": []},
                    {"name": "tilde", "kinks": []},
                    {"name": "no", "kinks": []},
                ]
            ),
        }
        response = self.client.post(
            reverse("kinks:kink_list_save", args=(kink_list1.id,)), editor_data
        )
        self.assertRedirects(response, kink_list1.get_absolute_url())
        response = self.client.post(
            reverse("kinks:kink_list_save", args=(kink_list2.id,)), editor_data
        )
        self.assertRedirects(response, kink_list2.get_absolute_url())

    def test_password_editing(self):
        orig_edit_password = "very_insecure"
        list_args = dict(edit_password=make_password(orig_edit_password))
        (
            custom_description,
            custom_name,
            kink_list,
            standard_description,
            standard_name,
        ) = make_test_data(list_args)
        view_password = "insecure"
        edit_password = "also_insecure"

        response = self.client.get(kink_list.get_absolute_url())
        self.assertContains(response, standard_name)
        self.assertContains(response, custom_name)

        self.client.post(
            reverse("kinks:kink_list_edit", args=(kink_list.id,)),
            {"edit-password": orig_edit_password},
        )

        editor_data = {
            "view-password": view_password,
            "edit-password": edit_password,
            "kink-list-data": json.dumps(
                [
                    {
                        "name": "heart",
                        "kinks": [{"custom": False, "id": Kink.objects.get().id}],
                    },
                    {"name": "check", "kinks": []},
                    {"name": "tilde", "kinks": []},
                    {
                        "name": "no",
                        "kinks": [
                            {
                                "custom": True,
                                "name": custom_name,
                                "description": custom_description,
                            }
                        ],
                    },
                ]
            ),
        }

        response = self.client.post(
            reverse("kinks:kink_list_save", args=(kink_list.id,)), editor_data
        )
        self.assertRedirects(
            response, kink_list.get_absolute_url(), target_status_code=403
        )

        kink_list.refresh_from_db()

        self.assertTrue(check_password(view_password, kink_list.view_password))
        self.assertTrue(check_password(edit_password, kink_list.edit_password))
