from django.urls import path
from . import views
from book.views import *
app_name="book"


urlpatterns = [
    path('userbooklist/', views.UserBookList.as_view()),
    path('create_book/',views.BookCreate.as_view()),
    path('get_book/<int:id>/', views.BookGetDetails.as_view()),
    path('update_book/<int:id>/', views.BookUpdate.as_view()),
    path('delete_book/<int:id>/', views.BookDelete.as_view()),
    path('all_book/', AllBookFilterView.as_view()),


    
    path('user_givingbookslist_host/', views.UserBookAvaliableToGive.as_view()),
    path('all_avaliable_books/', views.GetAllAvaliableBooks.as_view()),
    path('create_exchange_request/',views.ExchangeRequestCreate.as_view()), 
    path('users_exchange_requests/',views.UsersBookExchangeRequestsList.as_view()), 
    path('delete_user_requests/<int:bookid>/', views.UserExchangeRequestDelete.as_view()),


    path('view_host_exchange_requests/', views.HostViewExchangeRequests.as_view()),
    path('update_exchange_requests/<int:resv_id>/', views.HostUpdateRequestStatus.as_view()),
]
