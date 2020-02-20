from django.contrib.admin import ModelAdmin, site

from order.models import Order


class OrderAdmin(ModelAdmin):

    list_display = ("master_type", "status_code", "date_created",
                    "date_modified", "request_date_from", "request_date_to",
                    "city", "selection_date", "description",
                    "client",)
    filter_horizontal = ("photo",)


site.register(Order, OrderAdmin)
