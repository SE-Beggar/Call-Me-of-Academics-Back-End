from django.urls import path

from paper.views import PaperView
from user.views import *

urlpatterns = [
    path('paperdetails/', csrf_exempt(PaperView.as_view())),
]