from django import forms

from order.models import OrderPhoto


class DocumentForm(forms.ModelForm):
    class Meta:
        model = OrderPhoto
        fields = ('description', 'image', )