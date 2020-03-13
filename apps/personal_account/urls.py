from django.urls import path

from apps.personal_account.views import (Registration, Confirmation, Logout,
                                         IsValidToken, Masters, Clients)

urlpatterns = [
    path('', IsValidToken.as_view()),
    path('registration/', Registration.as_view()),
    path('confirmation/', Confirmation.as_view()),
    path('logout/', Logout.as_view()),
    path('masters/<int:master_id>/', Masters.as_view(), name='masters'),
    path('clients/<int:client_id>/', Clients.as_view(), name="clients")
]
