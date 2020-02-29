from django.contrib.admin import ModelAdmin, site

from manuals.models import (MasterType, UserType, OrderStatus,
                            MasterStatus, UserStatus, City)


class MasterTypeAdmin(ModelAdmin):

    list_display = ("id", "name")


class UserTypeAdmin(ModelAdmin):

    list_display = ("code", "name")


class UserStatusAdmin(ModelAdmin):

    list_display = ("code", "name")


class OrderStatusAdmin(ModelAdmin):

    list_display = ("code", "name")


class MasterStatusAdmin(ModelAdmin):

    list_display = ("code", "name")


class CityAdmin(ModelAdmin):

    list_display = ("id", "name")


site.register(MasterType, MasterTypeAdmin)
site.register(MasterStatus, MasterStatusAdmin)
site.register(OrderStatus, OrderStatusAdmin)
site.register(UserStatus, UserStatusAdmin)
site.register(UserType, UserTypeAdmin)
site.register(City, CityAdmin)
