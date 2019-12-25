from django.contrib.admin import ModelAdmin, site

from personal_account.models import User, PhoneCode


class UserAdmin(ModelAdmin):

    list_display = ("id", "phone_number", "is_active", "date_joined")


class PhoneCodeAdmin(ModelAdmin):

    list_display = ("id", "user_id", "code", "query_time")


site.register(User, UserAdmin)
site.register(PhoneCode, PhoneCodeAdmin)
