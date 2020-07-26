from django.urls import path

from apps.feedbacks.views import FeedBackView, NotificationView

urlpatterns = [
    path('masters/<int:master_id>/', FeedBackView.as_view()),
    path('notifications/', NotificationView.as_view())
]
