from django.urls import path

from apps.users.views import (RegistrationView, ConfirmationView, LogoutView,
                              IsValidTokenView, MastersView, ClientsView,
                              MasterSettingsView, ClientSettingsView, LogoutAll)

urlpatterns = [
    path('', IsValidTokenView.as_view()),
    path('registration/', RegistrationView.as_view()),
    path('confirmation/', ConfirmationView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('masters/<int:master_id>/', MastersView.as_view(), name='masters'),
    path('clients/<int:client_id>/', ClientsView.as_view(), name='clients'),
    path('masters/<int:master_id>/settings/', MasterSettingsView.as_view()),
    path('clients/<int:client_id>/settings/', ClientSettingsView.as_view()),
    path('logoutAll/', LogoutAll.as_view())
]
