from django.urls import path
from . import views
from comments.views import *
app_name="comments"

    
urlpatterns = [
    path('create_comment/',views.CommentCreate.as_view()),
    path('get_comment/<int:id>/', views.CommentGetDetails.as_view()),
    path('update_comment/<int:id>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:id>/', views.CommentDelete.as_view()),
    path('all_comment/', views.AllCommentFilterView.as_view()),
    path('user_comments/', views.CommentList.as_view()),
]
