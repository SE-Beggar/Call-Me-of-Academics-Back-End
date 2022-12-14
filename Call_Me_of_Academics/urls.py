"""Call_Me_of_Academics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import paper.views
import user.views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/user/', include(('user.urls', 'user'))),
    path('api/paper/', include(('paper.urls', 'paper'))),
    path('api/collection/search/', paper.views.VenueSearchView.as_view()),
    path('api/collection/list/', paper.views.VenueDetailView.as_view()),
    path('api/admin/identify/', user.views.IdentifyView.as_view()),
]
