from django.urls import path

from apps.manuals.views import CityView, MasterTypeView

urlpatterns = [
    path('', CityView.as_view()),
    path('cities/', CityView.as_view()),
    path('typeMasters/', MasterTypeView.as_view())
]
