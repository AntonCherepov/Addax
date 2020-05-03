from django.contrib.admin import ModelAdmin, site

from manuals.models import MasterType, OrderStatus, City


class MasterTypeAdmin(ModelAdmin):

    list_display = ("id", "name")


class OrderStatusAdmin(ModelAdmin):

    list_display = ("code", "name")


class CityAdmin(ModelAdmin):

    list_display = ("id", "name")


site.register(MasterType, MasterTypeAdmin)
site.register(OrderStatus, OrderStatusAdmin)
site.register(City, CityAdmin)
