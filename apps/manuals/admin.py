from django.contrib.admin import ModelAdmin, site

from manuals.models import MasterType, City


class MasterTypeAdmin(ModelAdmin):

    list_display = ("id", "name")


class CityAdmin(ModelAdmin):

    list_display = ("id", "name")


site.register(MasterType, MasterTypeAdmin)
site.register(City, CityAdmin)
