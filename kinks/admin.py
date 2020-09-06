from django.contrib import admin

from .models import KinkCategory, Kink, KinkList, CustomKinkListEntry, CustomReject

# Register your models here.
admin.site.register(KinkCategory)
admin.site.register(Kink)
admin.site.register(KinkList)


def reject_custom(modeladmin, request, queryset):
    names = set(x.custom_name for x in queryset)
    for name in names:
        CustomReject.objects.create(name=name)
        CustomKinkListEntry.objects.filter(custom_name__iexact=name).delete()


reject_custom.short_description = "Reject selected custom kinks"


class CustomKinkListEntryAdmin(admin.ModelAdmin):
    actions = [reject_custom]


admin.site.register(CustomKinkListEntry, CustomKinkListEntryAdmin)
admin.site.register(CustomReject)
