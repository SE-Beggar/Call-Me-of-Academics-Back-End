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
from django.urls import path, include, re_path
from django.views.static import serve

import paper.views
import user.views
from Call_Me_of_Academics import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('user/', include(('user.urls', 'user'))),
    path('paper/', include(('paper.urls', 'paper'))),
    path('collection/search/', paper.views.VenueSearchView.as_view()),
    path('collection/list/', paper.views.VenueDetailView.as_view()),
    path('admin/identify/', user.views.IdentifyView.as_view()),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
