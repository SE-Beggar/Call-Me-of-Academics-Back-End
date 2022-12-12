from django.urls import path

from paper.views import SearchPaperView, SearchAuthorView

urlpatterns = [
    path('searchpaper/', SearchPaperView.as_view()),
    path('searchscholar/', SearchAuthorView.as_view()),
]