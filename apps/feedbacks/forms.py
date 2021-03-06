from time import time

from django.forms import ModelForm

from feedbacks.models import FeedBack

now = int(time())


class FeedBackForm(ModelForm):

    class Meta:
        model = FeedBack
        exclude = ('client', 'master', 'date_created', 'comment')
