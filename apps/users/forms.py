from django.forms import Form, CharField, IntegerField


class RegistrationForm(Form):
    phone = CharField(min_length=10, max_length=10)
    type_code = CharField(max_length=1)


class ConfirmationForm(Form):
    phone = CharField(min_length=10, max_length=10)
    code = IntegerField(min_value=100000, max_value=999999)
