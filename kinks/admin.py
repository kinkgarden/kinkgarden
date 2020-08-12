from django.contrib import admin

from .models import KinkCategory, Kink, KinkList

# Register your models here.
admin.site.register(KinkCategory)
admin.site.register(Kink)
admin.site.register(KinkList)
