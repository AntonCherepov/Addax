from django.urls import path

from apps.feedbacks.views import FeedBackView

urlpatterns = [
    path('masters/<int:master_id>/', FeedBackView.as_view()),
]
