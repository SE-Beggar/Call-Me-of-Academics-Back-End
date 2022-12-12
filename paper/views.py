from django.http import JsonResponse
from django.shortcuts import render
from django_elasticsearch_dsl_drf.filter_backends import DefaultOrderingFilterBackend, FacetedSearchFilterBackend, \
    FilteringFilterBackend, SearchFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch_dsl import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from paper.documents import PaperDocument, AuthorDocument
from paper.serializers import PaperSerializer, AuthorSerializer


# Create your views here.
def get_paper_detail(request):
    if request.method == 'GET':
        paper_id = request.GET.get('paperid')
        search = PaperDocument.search(index='paper').query("match", id=paper_id)
        response = search.execute()
        return JsonResponse(PaperSerializer(instance=response.hits[0]).data)


class SearchPaperView(APIView):
    def post(self, request):
        data = request.data
        q = Q('multi_match', query=data['title'],
              fields=[
                  'title',
                  'authors.name',
                  'venue.raw',
                  'publisher',
                  'abstract',
                  'keywords'
              ])
        type_selected = data.get('typeSelected', None)
        year_selected = data.get('yearSelected', None)
        search = PaperDocument.search(index='paper').query(q)
        if type_selected:
            search = search.filter('terms', doc_type=type_selected)
        if year_selected:
            search = search.filter('terms', year=year_selected)
        response = search.execute()
        print('HitNum:', len(response.hits))
        serializer = PaperSerializer(instance=response.hits, many=True)
        return Response(serializer.data)


class SearchAuthorView(APIView):
    def post(self, request):
        data = request.data
        q = Q('multi_match', query=data['scholar'],
              fields=[
                  'name',
                  'orgs',
                  'tags.t'
              ])
        search = AuthorDocument.search(index='author').query(q)
        response = search.execute()
        print('HitNum:', len(response.hits))
        serializer = AuthorSerializer(instance=response.hits, many=True)
        return Response(serializer.data)


# class PaperViewSet(DocumentViewSet):
#     document = PaperDocument
#     serializer_class = PaperSerializer
#     ordering = ('_id',)
#     lookup_field = 'id'
#
#     filter_backends = [
#         DefaultOrderingFilterBackend,
#         FilteringFilterBackend,
#         SearchFilterBackend,
#     ]
#
#     search_fields = (
#         'title',
#         'authors.name',
#         'venue.raw',
#         'publisher'
#         'abstract',
#         'keywords'
#     )
#
#     filter_fields = {
#         'title': 'title',
#     }
