from django.urls import path, include
from accounts import views
from .views import popular_board, recommend_board, reque_post, reque_delete, create_curation ,reque_update,request_board, reque_search, recom_search, recom_detail, recom_post, recom_update, recom_delete, reque_detail, mypage, count_bookmark

app_name = "playlistApp"

urlpatterns = [
    path('popular_board/', popular_board, name='popular_board'),
    path('recommend_board/', recommend_board, name='recommend_board'),
    path('recommend_detail/<int:id>/', recom_detail, name="recommend_detail"),
    path('create_recommend', recom_post, name='create_recommend'),
    path('update_recommend/<int:id>/', recom_update, name='update_recommend'),
    path('delete_recommend/<int:id>/', recom_delete, name='delete_recommend'),
    path('reque_post/', reque_post, name='reque_post'),
    path('request_board/', request_board, name='request_board'),
    path('reque_detail/<int:id>/', reque_detail, name='reque_detail' ),
    path('update_request/<int:id>/', reque_update, name='update_request'),
    path('delete_request/<int:id>/', reque_delete, name='delete_request'),
    path('reque_search/', reque_search, name='reque_search'),
    path('recom_search/', recom_search, name='recom_search'),
    path('mypage/', mypage, name='mypage'),
    path('create_curation/<int:id>/', create_curation, name='create_curation'),
    path('count_bookmark/<int:id>/', count_bookmark, name='count_bookmark'),
]