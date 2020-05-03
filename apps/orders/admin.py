from django.contrib.admin import ModelAdmin, site

from orders.models import Order


class OrderAdmin(ModelAdmin):

    list_display = ("master_type", "status", "date_created",
                    "date_modified", "request_date_from", "request_date_to",
                    "city", "selection_date", "description",
                    "client",)


site.register(Order, OrderAdmin)
