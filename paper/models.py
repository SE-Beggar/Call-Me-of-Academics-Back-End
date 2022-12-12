from django.db import models


# Create your models here.

class Author(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=10, default='')
    n_pubs = models.IntegerField()
    n_citations = models.IntegerField()
    h_index = models.IntegerField()


class Venue(models.Model):
    id = models.CharField(max_length=25, primary_key=True)


class Keyword(models.Model):
    keyword = models.CharField(max_length=50)


class Url(models.Model):
    url = models.URLField()


class Paper(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField(Author, through='Paper_Author')
    venue = models.ManyToManyField(Venue)
    year = models.IntegerField(default=0)
    keywords = models.ManyToManyField(Keyword)
    n_citation = models.IntegerField(default=0)
    page_start = models.CharField(max_length=10, default='')
    page_end = models.CharField(max_length=10, default='')
    doc_type = models.CharField(max_length=10, default='')
    lang = models.CharField(max_length=10, default='')
    publisher = models.CharField(max_length=20, default='')
    volume = models.CharField(max_length=10, default='')
    issue = models.CharField(max_length=10, default='')
    issn = models.CharField(max_length=10, default='')
    isbn = models.CharField(max_length=20, default='')
    doi = models.CharField(max_length=20, default='')
    pdf = models.CharField(max_length=50, default='')
    url = models.ManyToManyField(Url)
    abstract = models.TextField(default='')


class Paper_Author(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    order = models.IntegerField()


