from rest_framework import viewsets
from django.shortcuts import get_object_or_404


from ..models import (
    User, 
    Survey, 
    Question, 
    Customer,
    Answer,
    CustomerAnswer,
    TakenSurvey)
from .serializers import (
    UserSerializer, 
    SurveySerializer, 
    QuestionSerializer, 
    AnswerSerializer,
    QuestionAnswerSerializer,
    CustomerAnswerSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class QuestionAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionAnswerSerializer
    queryset = TakenSurvey.objects.all()
    http_method_names = ['get',]


class CustomerAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerAnswerSerializer
    queryset = CustomerAnswer.objects.all()

    def create(self, request):
        customer = request.data.get('customer')
        answer = request.data.get('answer')
        customer = get_object_or_404(Customer, pk=customer)
        survey = get_object_or_404(Answer, pk=answer).question.survey
        customer.surveyes.add(survey)
        TakenSurvey.objects.create(
                                    customer=customer,
                                    survey=survey
                                )
        return super().create(request)