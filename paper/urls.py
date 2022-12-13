from django.urls import path

from paper.views import SearchPaperView, SearchAuthorView, PaperDetailView, AuthorDetailView, AuthorRelationshipView, \
    PaperSuggestionsView

urlpatterns = [
    path('paperdetails/', PaperDetailView.as_view()),
    path('searchpaper/', SearchPaperView.as_view()),
    path('searchscholar/', SearchAuthorView.as_view()),
    path('scholar/', AuthorDetailView.as_view()),
    path('scholarrelationship/', AuthorRelationshipView.as_view()),
    path('preview/', PaperSuggestionsView.as_view())
]