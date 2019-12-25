from django.urls import path

from apps.personal_account.views import Registration, Confirmation, Logout
from .views import default

urlpatterns = [
    path('', default, name='default'),
    path('reg', Registration.as_view()),
    path('confirm', Confirmation.as_view()),
    path('logout', Logout.as_view()),
]
