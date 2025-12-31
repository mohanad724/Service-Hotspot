from django.urls import path

from .views import UserRegistrationView,LoginView,UserDetailView,UserUpdateView,LogoutView
from .views import user_redirect_view


app_name = "users"
urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('login/',LoginView.as_view(), name='user-login' ),
    path('UserDetail/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('logout/',LogoutView.as_view(), name= 'user-logout'),
    path("~redirect/", view=user_redirect_view, name="redirect")
]
