from django.urls import path

from paper.views import SearchPaperView, SearchAuthorView, PaperDetailView, AuthorDetailView, AuthorRelationshipView, \
    PaperSuggestionsView, IndexView, AdvancedSearchView

urlpatterns = [
    path('paperdetails/', PaperDetailView.as_view()),
    path('searchpaper/', SearchPaperView.as_view()),
    path('searchscholar/', SearchAuthorView.as_view()),
    path('scholar/', AuthorDetailView.as_view()),
    path('scholarrelationship/', AuthorRelationshipView.as_view()),
    path('preview/', PaperSuggestionsView.as_view()),
    path('main/', IndexView.as_view()),
    path('advancesearch/', AdvancedSearchView.as_view())
]