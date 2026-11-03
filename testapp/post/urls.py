from django.urls import path, re_path

from .views import (
    PostDetailView,
    PostListView,
    createpost_view,
)

app_name = "post"

urlpatterns = [
    path("", PostListView.as_view(), name="postlist"),
    path("createpost/", createpost_view, name="createpost"),
    re_path(r"(?P<slug>[\w-]+)/$", PostDetailView.as_view(), name="postdetail"),
]
