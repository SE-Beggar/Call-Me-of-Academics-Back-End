from django.urls import path

from user.views import *

urlpatterns = [
    path('register/', csrf_exempt(RegisterView.as_view())),
    path('login/', login),
    path('logout/', logout),
    path('userspace/', csrf_exempt(InfoView.as_view())),
    path('identify/', ApplicationView.as_view())
]