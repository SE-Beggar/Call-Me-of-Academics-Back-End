from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from elasticsearch import Elasticsearch
from rest_framework.views import APIView


class PaperView(APIView):

    def get(self, request):
        id = request.GET.get('paperid')
        print(id)
        es = Elasticsearch(['http://localhost:9200/'])
        body = {
            "size": 200,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "id": id,
                            }
                        },
                    ]
                }
            },
        }
        res = es.search(body=body)
        print(res)
        return JsonResponse(res["hits"]["hits"][0]["_source"])