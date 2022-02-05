from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

from ..models import User, Survey
from .serializers import UserSerializer, SurveySerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def create(self, request):
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            survey = serializer.create(request)
            if survey:
                return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)