from django.urls import path

from myapp.views import PatternListView, CaughtMessageCreateView

urlpatterns = [
    path("patterns/", PatternListView.as_view(), name="pattern-list"),
    path(
        "caught-messages/",
        CaughtMessageCreateView.as_view(),
        name="caught-message-create",
    ),
]
