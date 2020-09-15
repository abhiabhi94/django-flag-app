from django.urls import path

from flag.views import SetFlag

app_name = 'flag'

urlpatterns = [
    path('', SetFlag.as_view(), name='flag'),
]
