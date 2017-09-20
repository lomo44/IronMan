from django.conf.urls import include,url
from .views import fb_echo
urlpatterns = [
    url(r"^webhook/?$", fb_echo.as_view())
]
