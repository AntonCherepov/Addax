from django.urls import path

from apps.feedbacks.views import FeedBackView

urlpatterns = [
    path('masters/<int:master_id>/feedbacks/', FeedBackView.as_view()),

]
