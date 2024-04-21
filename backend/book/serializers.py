from rest_framework import serializers
import book.models
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, IntegerField


"""
Serializers for Books
"""

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')
    
class BookCreateSerializer(ModelSerializer):

    """
    Serializer for creating books owned by a user.
    """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = book.models.Book
        fields =    ["name", "description", "image", "genre", "owner"]


class UserBookListSerializer(ModelSerializer):

    """
    Serializer for listing created books by user.
    """
        
    class Meta:
        model = book.models.Book
        fields =    ['id',"name", "description", "avaliable_to_give", "genre", "owner"]


class BookUpdateSerializer(ModelSerializer):

    """
    Serializer for updating created books by user.
    """
    class Meta:
        model = book.models.Book
        fields =    ["name", "description", "avaliable_to_give", "genre"]


class BookDeleteSerializer(ModelSerializer):

    """
    Serializer for deleting created books by user.
    """    
    class Meta:
        model = book.models.Book
        fields =    ["name", "description", "owner"]


class AllBookListSerializer(ModelSerializer):
    class Meta:
        model = book.models.Book
        fields =    ['id', "name",  "description", "avaliable_to_give", "genre", "owner"]





"""
Serializers to handle Exchange/Give Book Request
"""


class UserBookAvaliableToGiveSerializer(ModelSerializer): #Book you want to rent out

    """
    Serializer for listing created books by user that user wants to exchange to others.
    """
    class Meta:
        model = book.models.Book
        fields =    ['id', "name","avaliable_to_give", "owner"]



class GetAllAvaliableBooksList(ModelSerializer):
    """
    Serializer for listing ALL avaliable books that can be exchanged.
    """
    class Meta:
        model = book.models.Book
        fields =    ['id', "name", "description", "genre", "avaliable_to_give", "owner"]


class CreateExchangeRequest(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    start_date = DateTimeField(validators=[required])
    end_date = DateTimeField(validators=[required])
    book_id = IntegerField(validators=[required])
    
    class Meta:
        model = book.models.ExchangeRequest
        fields =    ['start_date', 'end_date', 'book_id', 'user']



class UsersBookExchangeRequestsSerializer(ModelSerializer): #Books you want to exchange from others
    """
    Serializer for creating an exchange request
    """
    class Meta:
        model = book.models.ExchangeRequest
        fields =    ['start_date', 'end_date', 'book_id']


class UserExchangeRequestDeleteSerializer(ModelSerializer):
    class Meta:
        model = book.models.ExchangeRequest
        fields =    ['start_date', 'end_date', 'book_id', 'status', 'user']





class HostViewExchangeRequestsSerializer(ModelSerializer):

    """
    Serializer for viewing an exchange request from other user
    """

    class Meta:
        model = book.models.ExchangeRequest
        fields =   ['id', 'start_date', 'end_date', 'book_id', 'status', 'user']

class HostExchangeRequestUpdateSerializer(ModelSerializer):
    """
    Serializer for updating/approving an exchange request from other user
    """
    class Meta:
        model = book.models.ExchangeRequest
        fields =   ['status']
