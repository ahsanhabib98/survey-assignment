from django.urls import path
from . import views as user_views

urlpatterns = [
    path('register/', user_views.RegisterAPIView.as_view(), name="register"),
    path('login/', user_views.LoginAPIView.as_view(), name="login"),
    path('logout/', user_views.LogoutAPIView.as_view(), name="logout"),
]