from django.urls import include, path

from .views import SignUpView, AdminSignUpView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/admin/', AdminSignUpView.as_view(), name='admin_signup'),
]
