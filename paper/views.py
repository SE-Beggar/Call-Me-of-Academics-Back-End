from django.http import JsonResponse

from elasticsearch_dsl import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from paper.documents import PaperDocument, AuthorDocument, VenueDocument
from paper.serializers import PaperSerializer, AuthorSerializer, VenueSerializer, VenueDetailSerializer, PubSerializer


class IndexView(APIView):
    def get(self, request):
        search = PaperDocument.search()[0:500].query('match_all').sort('-n_citation')
        response = search.execute()
        return Response({'errno': 0, 'papers': PubSerializer(instance=response.hits, many=True).data})


# Create your views here.
class PaperDetailView(APIView):
    def get(self, request):
        paper_id = request.query_params.get('paperid')
        search = PaperDocument.search()[0:500].filter("term", id=paper_id)
        response = search.execute()
        return JsonResponse({'errno': 0, 'paper': PaperSerializer(instance=response.hits[0]).data})


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
        search = PaperDocument.search(index='paper')[0:100].query(q)
        if type_selected:
            search = search.filter('terms', doc_type=type_selected)
        if year_selected:
            search = search.filter('terms', year=year_selected)
        response = search.execute()
        print('HitNum:', len(response.hits))
        serializer = PaperSerializer(instance=response.hits, many=True)
        return Response({'errno': 0,'papers': serializer.data})


class SearchAuthorView(APIView):
    def post(self, request):
        data = request.data
        q = Q('multi_match', query=data['scholar'],
              fields=[
                  'name',
                  'orgs',
                  'tags.t'
              ])
        search = AuthorDocument.search()[0:500].query(q)
        response = search.execute()
        print('HitNum:', len(response.hits))
        serializer = AuthorSerializer(instance=response.hits, many=True)
        return Response({'errno': 0,'scholars': serializer.data})


class AdvancedSearchView(APIView):
    def post(self, request):
        content = request.data['advancecontent']
        must = []
        should = []
        for item in content:
            if item['logic']:
                if item['entry'] == 0:
                    should.append(Q('match', title=item['input']))
                elif item['entry'] == 1:
                    should.append(Q('match', abstract=item['input']))
                elif item['entry'] == 2:
                    should.append(Q('match', **{'author.name': item['input']}))
                elif item['entry'] == 3:
                    should.append(Q('match', **{'venue.raw': item['input']}))
            else:
                if item['entry'] == 0:
                    should.append(Q('match', title=item['input']))
                elif item['entry'] == 1:
                    should.append(Q('match', abstract=item['input']))
                elif item['entry'] == 2:
                    should.append(Q('match', **{'author.name': item['input']}))
                elif item['entry'] == 3:
                    should.append(Q('match', **{'venue.raw': item['input']}))
            search = PaperDocument.search()[0:500].query('bool', must=must, should=should)
            response = search.execute()
            print('HitNum:', len(response.hits))
            serializer = PaperSerializer(instance=response.hits, many=True)
            return Response({'errno': 0,'papers': serializer.data})


class AuthorDetailView(APIView):
    def post(self, request):
        author_id = request.data.get('id')
        search = AuthorDocument.search()[0:500].filter('term', id=author_id)
        response = search.execute()

        print(response.hits)
        return Response({'errno': 0, 'scholar': AuthorSerializer(instance=response.hits[0]).data})


class AuthorRelationshipView(APIView):
    def post(self, request):
        author_id = request.data.get('id')
        search = AuthorDocument.search()[0:500].filter('term', id=author_id)
        response = search.execute()
        author = response.hits[0]
        pub_id_list = [
            pub['i'] for pub in author.pubs
        ]
        search = PaperDocument.search()[0:500].filter('terms', id=pub_id_list)
        print(pub_id_list)
        ret = []
        for paper_doc in search:
            for author in paper_doc.authors:
                author_dict = {
                    'id': author['id'],
                    'name': author['name']
                }
                ret .append(author_dict)
        ret = [dict(t) for t in set([tuple(d.items()) for d in ret])]
        return Response({'errno': 0, 'scholars': ret})


class VenueSearchView(APIView):
    def post(self, request):
        venue_name = request.data.get('name')
        q = Q('multi_match', query=venue_name, fields=['DisplayName', 'NormalizedName'])
        search = VenueDocument.search()[0:500].query(q)
        response = search.execute()
        print('HitNum:', len(response.hits))
        serializer = VenueSerializer(instance=response.hits, many=True)
        return Response({'errno': 0, 'venues': serializer.data})


class VenueDetailView(APIView):
    def get(self, request):
        venue_id = request.query_params.get('id')
        search = VenueDocument.search()[0:500].filter('term', id=venue_id)
        response = search.execute()
        return Response({'errno': 0, 'venue': VenueDetailSerializer(instance=response.hits[0]).data})


class PaperSuggestionsView(APIView):
    def post(self, request):
        input = request.data.get('input')
        if input:
            print(input)
            search = PaperDocument.search()[0:500].suggest('suggest', input, term={'field': 'title.suggest'})
            response = search.execute()
            options = response.suggest['suggest'][0]['options']
            text_list = [
                item['text'] for item in options
            ]
            return Response({'errno': 0, 'list': text_list})




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
