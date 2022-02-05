from django.urls import include, path

from survey.views import survey, customers, admins

urlpatterns = [
    path('', include('survey.urls')),
    path('api', include('survey.api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', survey.SignUpView.as_view(), name='signup'),
    path('accounts/signup/customer/', customers.CustomerSignUpView.as_view(), name='customer_signup'),
    path('accounts/signup/admin/', admins.AdminSignUpView.as_view(), name='admin_signup'),
]
