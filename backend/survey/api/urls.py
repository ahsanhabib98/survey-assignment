from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SurveyViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', UserViewSet, base_name='users')
router.register(r'', SurveyViewSet, base_name='surveys')


urlpatterns = router.urls