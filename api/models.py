from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class ResponseTemplate(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Field(models.Model):
    TYPE_OF_FIELD_CHOICES = (
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('text', 'Text'),
        ('file', 'File'),
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    type_of_field = models.CharField(max_length=50, choices=TYPE_OF_FIELD_CHOICES)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = slugify(self.title)
        super(Field, self).save(*args, **kwargs)


class ResponseTemplateField(models.Model):
    response_template = models.ForeignKey(ResponseTemplate, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)


class Query(models.Model):
    text = models.TextField()
    description = models.TextField()
    response_type = models.ForeignKey(ResponseTemplate, on_delete=models.CASCADE)
    max_responses = models.PositiveIntegerField(default=0)
    required = models.BooleanField(default=False)

    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Response(models.Model):
    response_template = models.ForeignKey(ResponseTemplate, on_delete=models.CASCADE)
    data = JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save_response(self, field, response):
        self.data[field] = response
        self.save()


class QueryResponse(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    responses = models.ManyToManyField(Response, through='QueryResponseThrough')

    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QueryResponseThrough(models.Model):
    query_response = models.ForeignKey(QueryResponse, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)


class Block(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()


class FormBlock(Block):
    queries = models.ManyToManyField(Query, through='FormQueryThrough')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    response_accept_ends_at = models.DateTimeField(null=True, blank=True)
    response_accept_starts_at = models.DateTimeField(null=True, blank=True)

    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = slugify(self.title)
        super(FormBlock, self).save(*args, **kwargs)


class FormQueryThrough(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    form_block = models.ForeignKey(FormBlock, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)


class Campaign(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)


class CampaignStage(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    blocks = models.ManyToManyField(Block, through='CampaignStageBlockThrough')
    position = models.PositiveIntegerField(default=0)


class CampaignStageBlockThrough(models.Model):
    campaign_stage = models.ForeignKey(CampaignStage, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)
