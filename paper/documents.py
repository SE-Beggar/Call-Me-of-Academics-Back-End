from django_elasticsearch_dsl import Index, fields
from django_elasticsearch_dsl.documents import DocType

from paper.models import Paper, Author, Venue

paper_index = Index('paper')
paper_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@paper_index.doc_type
class PaperDocument(DocType):
    id = fields.KeywordField()
    title = fields.TextField(
        fields={
            'keyword': fields.KeywordField(),
            'suggest': fields.CompletionField()
        }
    )
    authors = fields.NestedField(
        properties={
            'id': fields.KeywordField(),
            'name': fields.TextField(
                fields={
                    'keyword': fields.KeywordField()
                }
            ),
            'org': fields.TextField(
                fields={
                    'keyword': fields.KeywordField()
                }
            )
        }
    )
    venue = fields.NestedField(
        properties={
            'id': fields.KeywordField(),
            'raw': fields.TextField(
                fields={
                    'keyword': fields.KeywordField()
                }
            )
        }
    )
    year = fields.IntegerField()
    keywords = fields.KeywordField()
    n_citation = fields.IntegerField()
    n_download = fields.IntegerField()
    page_start = fields.KeywordField()
    page_end = fields.KeywordField()
    doc_type = fields.KeywordField()
    lang = fields.KeywordField()
    publisher = fields.KeywordField()
    volume = fields.KeywordField()
    issue = fields.KeywordField()
    issn = fields.KeywordField()
    isbn = fields.KeywordField()
    doi = fields.KeywordField()
    pdf = fields.KeywordField()
    url = fields.KeywordField()
    abstract = fields.TextField()

    class Django:
        model = Paper


author_index = Index('author')
author_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@author_index.doc_type
class AuthorDocument(DocType):
    id = fields.KeywordField()
    name = fields.TextField(
        fields={
            'keyword': fields.KeywordField()
        }
    )
    orgs = fields.TextField(
        fields={
            'keyword': fields.KeywordField()
        }
    )
    position = fields.KeywordField()
    n_pubs = fields.IntegerField()
    n_citation = fields.IntegerField()
    h_index = fields.IntegerField()
    identified = fields.IntegerField()
    tags = fields.NestedField(
        properties={
            "t": fields.TextField(
                fields={
                    'keyword': fields.KeywordField()
                }
            ),
            "w": fields.IntegerField()
        }
    )
    pubs = fields.NestedField(
        properties={
            'i': fields.KeywordField(),
            'r': fields.IntegerField()
        }
    )

    class Django:
        model = Author


venue_index = Index('venues')
venue_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@venue_index.doc_type
class VenueDocument(DocType):
    id = fields.KeywordField()
    DisplayName = fields.TextField(
        fields={
            'keyword': fields.KeywordField()
        }
    )
    NormalizedName = fields.TextField(
        fields={
            'keyword': fields.KeywordField()
        }
    )

    class Django:
        model = Venue



