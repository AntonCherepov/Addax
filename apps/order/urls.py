from django.urls import path

from apps.order.views import Replies, OrderView, OrderById

urlpatterns = [
    path('', OrderView.as_view()),
    path('<int:order_id>/', OrderById.as_view()),
    path('<int:order_id>/replies/', Replies.as_view())
]
