import debug_toolbar
from django.conf import settings
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('user/', include('user.urls')),
]

# URLs only used when DEBUG = True
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
