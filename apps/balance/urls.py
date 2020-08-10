from django.urls import path

from balance.views import GetMasterBalance

urlpatterns = [
    path('', GetMasterBalance.as_view()),
]
