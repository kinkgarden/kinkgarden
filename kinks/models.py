import enum
import uuid
from collections import namedtuple
import typing

from django.db import models


class KinkCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "kink categories"


class Kink(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    category = models.ForeignKey(
        KinkCategory, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


ConcreteKink = namedtuple("ConcreteKink", ["name", "description"])


class KinkListColumn(enum.Enum):
    HEART = enum.auto()
    CHECK = enum.auto()
    TILDE = enum.auto()
    NO = enum.auto()


class KinkList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    view_password = models.CharField(max_length=128, blank=True)
    edit_password = models.CharField(max_length=128, blank=True)
    example = models.BooleanField(default=False)
    short_link = models.CharField(max_length=32, blank=True, default="")

    def get_absolute_url(self):
        from django.urls import reverse

        if len(self.short_link) > 0:
            return reverse("kinks:kink_list_by_short_link", args=(self.short_link,))
        return reverse("kinks:kink_list", args=(self.id,))

    @property
    def columns(self) -> typing.List[typing.Tuple[str, typing.List[ConcreteKink]]]:
        standard_kinks = self.standardkinklistentry_set.all().select_related("kink")
        custom_kinks = self.customkinklistentry_set.all()

        column_data = dict((x, []) for x in KinkListColumn)
        for kink in standard_kinks:
            column_data[KinkListColumn(kink.column)].append(
                ConcreteKink(kink.kink.name, kink.kink.description)
            )
        for kink in custom_kinks:
            if not kink.admin_delete:
                column_data[KinkListColumn(kink.column)].append(
                    ConcreteKink(kink.custom_name, kink.custom_description)
                )

        return [
            (column_type.name.lower(), sorted(column_content, key=lambda x: x.name))
            for column_type, column_content in column_data.items()
        ]

    def __str__(self):
        return str(self.id)


class KinkListEntry(models.Model):
    COLUMNS = [(x.value, x.name.lower()) for x in KinkListColumn]

    list = models.ForeignKey(KinkList, on_delete=models.CASCADE)

    column = models.SmallIntegerField(choices=COLUMNS)

    class Meta:
        abstract = True


class StandardKinkListEntry(KinkListEntry):
    kink = models.ForeignKey(
        Kink, on_delete=models.CASCADE, related_name="+", null=True, blank=True
    )

    def __str__(self):
        return str(self.list) + " - " + str(self.kink)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["list", "kink"], name="unique_standard_kinks"
            )
        ]
        verbose_name_plural = "standard kink list entries"


class CustomKinkListEntry(KinkListEntry):
    custom_name = models.CharField(max_length=200, blank=True)
    custom_description = models.CharField(max_length=1000, blank=True)
    admin_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.list) + " - " + str(self.custom_name)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["list", "custom_name"], name="unique_custom_kinks"
            )
        ]
        verbose_name_plural = "custom kink list entries"
