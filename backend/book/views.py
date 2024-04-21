from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.exceptions import NotFound
# Create your views here.
from rest_framework.response import Response
from rest_framework import serializers, permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from book.models import *
from book.serializers import *

from rest_framework import filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user
from rest_framework.fields import empty
from .pagination import CustomPagination

class CheckBookExist(APIView, permissions.BasePermission):
    message = 'Book does not exist for user'

    def has_permission(self, request, view):
        all = book.models.Book.objects.filter(owner=request.user.id)
        if all:
            return True
        else:
            return False


class BookGetDetails(RetrieveAPIView): #Shows Details of a single book
    serializer_class = AllBookListSerializer

    def get_object(self):
        return get_object_or_404(Book, id=self.kwargs['id'])


class UserBookList(ListAPIView): #Shows OWNED books BY USER
    serializer_class = UserBookListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', "name", "genre"]
    def get_queryset(self):
        return book.models.Book.objects.filter(owner=self.request.user.id)


class AllBookFilterView(ListAPIView): #Display every book created
    queryset = Book.objects.all()
    pagination_class = CustomPagination
    serializer_class = AllBookListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', "name", "genre"]


     
class BookCreate(ListCreateAPIView): #CREATE BOOKS
    serializer_class = BookCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['owner'] = self.request.user.id
        return super().create(request, *args, **kwargs)
    """ 
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return book.models.Book.objects.filter(owner=self.request.user.id)


class BookUpdate(RetrieveUpdateAPIView):
    serializer_class = BookUpdateSerializer

    permission_classes = [IsAuthenticated, CheckBookExist]

    def get_object(self):
        user_id = self.request.user.id
        try:
            all = book.models.Book.objects.get(id=self.kwargs['id'])
        except:
            raise NotFound('ERROR: NOT FOUND')
        
        if all:
            if user_id != all.owner.id:
                raise NotFound("ERROR: PERMISSION DENIED")
            return all
        else:
            raise NotFound('ERROR: NOT FOUND')


class BookDelete(RetrieveDestroyAPIView):
    serializer_class = BookDeleteSerializer
    permission_classes = [IsAuthenticated, CheckBookExist]
    
    def get_object(self):
        user_id = self.request.user.id
        try:
            all = book.models.Book.objects.get(id=self.kwargs['id'])
        except:
            raise NotFound('ERROR: NOT FOUND')
        
        if all:
            if user_id != all.owner.id:
                raise NotFound("ERROR: PERMISSION DENIED")
            return all
        else:
            raise NotFound('ERROR: NOT FOUND')
        
       
class UserBookAvaliableToGive(ListAPIView): #Get book rented out to others by user
    serializer_class = UserBookAvaliableToGiveSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def get_queryset(self):
        gifting_books = book.models.Book.objects.filter(owner=self.request.user.id, avaliable_to_give=True)
        if not gifting_books:
            raise NotFound('ERROR: YOU DID NOT RENT OUT ANY BOOKS')
        return gifting_books



class GetAllAvaliableBooks(ListAPIView): 
    queryset = book.models.Book.objects.filter(avaliable_to_give=True)
    serializer_class = GetAllAvaliableBooksList
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def get_serializer(self, instance=None, data=empty, many=False, partial=False):
        return super(GetAllAvaliableBooks, self).get_serializer(instance=instance, data=data, many=True, partial=partial)


class ExchangeRequestCreate(ListCreateAPIView): #CREATE a request
    serializer_class = CreateExchangeRequest
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def create(self, request, *args, **kwargs):

        request.data._mutable = True
        try:
            propid = request.data['book_id']
            requested_reservation  = book.models.Book.objects.get(avaliable_to_give=True, id = propid) #book_id = id of book
            if not requested_reservation:
                return Response('ERROR : Book is unavailable to exchanged.')

            current_list_of_reservations = book.models.ExchangeRequest.objects.filter(user=self.request.user.id)
            id_list = [reservation.book_id for reservation in current_list_of_reservations]

            if int(propid) in id_list:
                return Response('ERROR : You have already exchanged this book')
        except:
            return Response('ERROR : Book is unavailable to exchanged')

        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        return book.models.ExchangeRequest.objects.filter(user=self.request.user.id)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    



    
class UsersBookExchangeRequestsList(ListAPIView): #List of books user wants (Made requests for those books)
    serializer_class = UsersBookExchangeRequestsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['start_date', 'end_date', 'book_id']

    def get_queryset(self):
        return book.models.ExchangeRequest.objects.filter(user=self.request.user.id)
    

class UserExchangeRequestDelete(RetrieveDestroyAPIView):
    serializer_class = UserExchangeRequestDeleteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user_id = self.request.user.id
        print(self.kwargs['bookid'])
        try:
            all = book.models.ExchangeRequest.objects.get(book_id=self.kwargs['bookid'],user=self.request.user.id)
            print(all.status)
        except:
            raise NotFound('ERROR: NOT FOUND')
        if all:
            if user_id != all.user.id:
                raise NotFound("ERROR: PERMISSION DENIED")
            return all
        else:
            raise NotFound('ERROR: NOT FOUND')






class HostViewExchangeRequests(ListAPIView): #Get book rented out to others by user
    serializer_class = HostViewExchangeRequestsSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'start_date', 'end_date', 'book_id', 'status', 'user']

    def get_queryset(self):
        gifting_books = book.models.Book.objects.filter(owner=self.request.user.id, avaliable_to_give=True)
        if not gifting_books:
            raise NotFound('ERROR: YOU DID NOT EXCHANGE/RENT OUT ANY BOOKS')
        
        exchanged_books_ids = [books.id for books in gifting_books]
        reservation_requests = book.models.ExchangeRequest.objects.filter(book_id__in = exchanged_books_ids)

        return reservation_requests
    

class HostUpdateRequestStatus(RetrieveUpdateAPIView):
    serializer_class = HostExchangeRequestUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        gifting_books = book.models.Book.objects.filter(owner=self.request.user.id, avaliable_to_give=True)
        if not gifting_books:
            raise NotFound('ERROR: YOU DID NOT EXCHANGE/RENT OUT ANY BOOKS')
        
        exchanged_books_ids = [books.id for books in gifting_books]
        reservation_requests = book.models.ExchangeRequest.objects.filter(book_id__in = exchanged_books_ids)
        #print(reservation_requests)

        user_id = self.request.user.id
        try:
            all = book.models.ExchangeRequest.objects.get(id=self.kwargs['resv_id'])
        except:
            raise NotFound('ERROR: NOT FOUND')
        
        if all:
            #print(all)
            if all not in reservation_requests:
                raise NotFound("ERROR: PERMISSION DENIED")
            return all
        else:
            raise NotFound('ERROR: NOT FOUND')

        

##TODO
##Delete book -> delete requests for that book
#Book Avaliability change to available start date and end dates