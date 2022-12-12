from django_elasticsearch_dsl_drf import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from paper.documents import PaperDocument, AuthorDocument
from paper.models import Paper


class PaperSerializer(DocumentSerializer):
    venue = serializers.ObjectField(required=False)
    year = serializers.IntegerField(required=False)
    keywords = serializers.CharField(required=False)
    n_citation = serializers.IntegerField(required=False)
    page_start = serializers.CharField(required=False)
    page_end = serializers.CharField(required=False)
    doc_type = serializers.CharField(required=False)
    lang = serializers.CharField(required=False)
    publisher = serializers.CharField(required=False)
    volume = serializers.CharField(required=False)
    issue = serializers.CharField(required=False)
    issn = serializers.CharField(required=False)
    isbn = serializers.CharField(required=False)
    doi = serializers.CharField(required=False)
    pdf = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    abstract = serializers.CharField(required=False)

    class Meta:
        document = PaperDocument
        fields = '__all__'


class AuthorSerializer(DocumentSerializer):
    orgs = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    n_citation = serializers.IntegerField(required=False)
    n_pubs = serializers.IntegerField(required=False)
    tags = serializers.ObjectField(required=False)
    class Meta:
        document = AuthorDocument
        fields = '__all__'
