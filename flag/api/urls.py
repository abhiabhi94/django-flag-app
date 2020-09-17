from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flag.api import views


urlpatterns = [
    path('flag/', views.SetFlag.as_view(),  name='flag'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
