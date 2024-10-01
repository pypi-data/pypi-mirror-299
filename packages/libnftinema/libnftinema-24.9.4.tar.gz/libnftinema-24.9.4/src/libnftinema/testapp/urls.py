from django.urls import path

from .views import SercurePostView
from .views import SimpleGetView

urlpatterns = [
    path("secure-post/", SercurePostView.as_view(), name="secure-post"),
    path("simple-get/", SimpleGetView.as_view(), name="simple-get"),
]
