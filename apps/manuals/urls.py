from django.urls import path

from apps.manuals.views import CityView

urlpatterns = [
    path('', CityView.as_view()),
    path('cities', CityView.as_view()),
    path('towns', CityView.as_view()),
]