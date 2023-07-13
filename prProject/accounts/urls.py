from django.contrib import admin
from django.urls import path
from accounts import views
from .views import kakao_get_login, get_user_info

app_name = "accounts"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login/kakao', kakao_get_login),
    path('login/kakao/user/callback/', get_user_info, name="kakao_callback"),
]
