from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts/", views.PostList.as_view(), name="posts"),
    path("posts/<slug:slug>", views.PostDetails.as_view(), name="detailed_post"),
    path("read_later", views.ReadLaterView.as_view(), name="read_later"),
]
