from django_elasticsearch_dsl_drf import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from elasticsearch_dsl import Q

from paper.documents import PaperDocument, AuthorDocument, VenueDocument
from paper.models import Paper
from user.models import User


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
    from rest_framework import serializers
    n_download = serializers.SerializerMethodField()

    def get_n_download(self, obj):
        if not obj.n_download:
            return 0
        else:
            return obj.n_download

    class Meta:
        document = PaperDocument
        fields = '__all__'


class PaperTitleSerializer(DocumentSerializer):

    class Meta:
        document = PaperDocument
        fields = (
            'id',
            'title',
        )


class PubSerializer(DocumentSerializer):
    venue = serializers.ObjectField(required=False)
    year = serializers.IntegerField(required=False)
    keywords = serializers.CharField(required=False)
    n_citation = serializers.IntegerField(required=False)
    n_download = serializers.IntegerField(default=0)
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
    class Meta:
        document = PaperDocument
        exclude = (
            'abstract'
        )


class AuthorSerializer(DocumentSerializer):
    orgs = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    n_citation = serializers.IntegerField(required=False)
    n_pubs = serializers.IntegerField(required=False)
    tags = serializers.ObjectField(required=False)
    from rest_framework import serializers
    pubs = serializers.SerializerMethodField()
    n_download = serializers.SerializerMethodField()
    isidentify = serializers.SerializerMethodField()

    def get_pubs(self, obj):
        # print('get_pubs')
        #print(obj.pubs)
        ret = []
        for item in obj.pubs:
            #print(item['i'])
            search = PaperDocument.search().filter('term', id=item['i'])
            response = search.execute()
            dict = item.to_dict()
            dict['r'] += 1
            #print(response.hits)
            if response.hits:
                dict.update(PubSerializer(instance=response.hits[0]).data)
            ret.append(dict)
        return ret

    def get_n_download(self, obj):
        num = 0
        for item in obj.pubs:
            search = PaperDocument.search().filter('term', id=item['i'])
            response = search.execute()
            #print(response.hits)
            if response.hits:
                for paper in response.hits:
                    if paper.n_download:
                        num += paper.n_download
        return num

    def get_isidentify(self, obj):
        if User.objects.filter(author_id=obj.id):
            return 1
        else:
            return 0

    class Meta:
        document = AuthorDocument
        fields = '__all__'


class AuthorSearchSerializer(DocumentSerializer):
    orgs = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    n_citation = serializers.IntegerField(required=False)
    n_pubs = serializers.IntegerField(required=False)
    tags = serializers.ObjectField(required=False)
    from rest_framework import serializers
    isidentify = serializers.SerializerMethodField()

    def get_isidentify(self, obj):
        if User.objects.filter(author_id=obj.id):
            return 1
        else:
            return 0

    class Meta:
        document = AuthorDocument
        fields = '__all__'


class VenueSerializer(DocumentSerializer):
    class Meta:
        document = VenueDocument
        fields = '__all__'


class VenueDetailSerializer(DocumentSerializer):
    from rest_framework import serializers
    papers = serializers.SerializerMethodField()

    def get_papers(self, obj):
        q = Q('nested', path='venue', query=Q('term', **{'venue.id': obj.id}))
        search = PaperDocument.search()[0:500].query(q)
        response = search.execute()
        return PubSerializer(instance=response.hits, many=True).data
    class Meta:
        document = VenueDocument
        fields = '__all__'

