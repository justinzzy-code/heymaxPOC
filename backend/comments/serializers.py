from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, IntegerField
from comments.models import Comment



"""
    Serializers for comments:
    Functions below include:

    1. Create Comments
    2. List All Comments
    3. Update Comment
    4. Delete Comment
    5. List ALL USER comments
"""


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'book_id', 'name', 'title', 'date', 'content',]

class AllCommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'book_id', 'name', 'title', 'date', 'content',]


class CommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['title','date', 'content',]


class CommentDeleteSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author','title','date', 'content',]


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields =  ['id', 'author', 'book_id', 'name', 'title', 'date', 'content',]





