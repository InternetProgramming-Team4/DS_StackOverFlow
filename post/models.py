from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Vote(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(default=uuid.uuid4)
    voted_object = GenericForeignKey('content_type', 'object_id')

    DOWNVOTE = -1
    UPVOTE = 1
    UNVOTE = 0
    VOTE_TYPE_CHOICES = ((DOWNVOTE, "Downvote"), (UPVOTE, "Upvote"), (UNVOTE, "Unvote"))
    score = models.IntegerField(choices=VOTE_TYPE_CHOICES, default=UNVOTE)
    voter = models.ForeignKey(User, related_name='post_votes', on_delete=models.CASCADE)


class Major(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/post/{self.slug}/'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    major = models.ForeignKey(Major, null=True, blank=False, on_delete=models.CASCADE)
    votes = GenericRelation(Vote, null=True, related_query_name='post')

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/post/{self.major.slug}/{self.pk}/'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(Vote, null=True, related_query_name='comment')

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
