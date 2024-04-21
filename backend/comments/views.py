from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import serializers, permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from comments.models import *
from comments.serializers import *

from rest_framework import filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user
from rest_framework.fields import empty
from book.pagination import CustomPagination

# Create your views here.

class CheckCommentExist(APIView, permissions.BasePermission):
    message = 'Comment does not exist for user'

    def has_permission(self, request, view):
        all = Comment.objects.filter(author=request.user.id)
        if all:
            return True
        else:
            return False
        


class CommentGetDetails(RetrieveAPIView): #Shows Details of a single comment
    serializer_class = AllCommentListSerializer

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['id'])
    

class AllCommentFilterView(ListAPIView): #Display every comment created
    queryset = Comment.objects.all()
    pagination_class = CustomPagination
    serializer_class = AllCommentListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'book_id', 'name', "author", "title", 'content',]
    

class CommentCreate(ListCreateAPIView): #Create comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user.id)
    

class CommentUpdate(RetrieveUpdateAPIView):
    serializer_class = CommentUpdateSerializer

    permission_classes = [IsAuthenticated, CheckCommentExist]

    def get_object(self):
        user_id = self.request.user.id
        try:
            all = Comment.objects.get(id=self.kwargs['id'])
        except:
            raise NotFound('ERROR: NOT FOUND')
        
        if all:
            if user_id != all.author.id:
                raise NotFound("ERROR: PERMISSION DENIED")
            return all
        else:
            raise NotFound('ERROR: NOT FOUND')


class CommentDelete(RetrieveDestroyAPIView):
    serializer_class = CommentDeleteSerializer
    permission_classes = [IsAuthenticated, CheckCommentExist]
    
    def get_object(self):
        user_id = self.request.user.id
        try:
            all = Comment.objects.get(id=self.kwargs['id'])
        except:
            raise NotFound('ERROR: NOT FOUND')
        
        if all:
            if user_id != all.author.id:
                raise NotFound("ERROR: PERMISSION DENIED")
            return all
        else:
            raise NotFound('ERROR: NOT FOUND')
        

class CommentList(ListAPIView): #Shows comments written BY USER
    serializer_class = CommentListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'author', 'book_id', 'name', 'title', 'date', 'content',]
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user.id)








    
    