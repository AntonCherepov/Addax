from django.contrib.admin import ModelAdmin, site

from users.models import User, PhoneCode


class UserAdmin(ModelAdmin):

    list_display = ("id", "phone_number", "date_joined")


class PhoneCodeAdmin(ModelAdmin):

    list_display = ("id", "user_id", "code", "query_time")


site.register(User, UserAdmin)
site.register(PhoneCode, PhoneCodeAdmin)
