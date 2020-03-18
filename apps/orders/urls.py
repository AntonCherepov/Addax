from django.urls import path

from apps.orders.views import RepliesView, OrderView, OrderByIdView

urlpatterns = [
    path('', OrderView.as_view()),
    path('<int:order_id>/', OrderByIdView.as_view()),
    path('<int:order_id>/replies/', RepliesView.as_view())
]
