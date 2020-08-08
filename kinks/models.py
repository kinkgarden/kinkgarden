from django.db import models


class KinkCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "kink categories"


class Kink(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(KinkCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
