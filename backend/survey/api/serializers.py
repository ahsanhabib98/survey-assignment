from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import User, Survey, Question, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_customer', 'is_admin')


class CustomRegisterSerializer(RegisterSerializer):
    is_customer = serializers.BooleanField()
    is_admin = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_customer', 'is_admin')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'is_customer': self.validated_data.get('is_customer', ''),
            'is_admin': self.validated_data.get('is_admin', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_customer = self.cleaned_data.get('is_customer')
        user.is_admin = self.cleaned_data.get('is_admin')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key', 'user', 'user_type')

    def get_user_type(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        is_customer = serializer_data.get('is_customer')
        is_admin = serializer_data.get('is_admin')
        return {
            'is_customer': is_customer,
            'is_admin': is_admin
        }


class AnswerSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'survey', 'answer_type', 'text', 'answer')

    def get_answers(self, obj):
        answers = AnswerSerializer(obj.answers.all(), many=True).data
        return answers


class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    owner = UserSerializer()

    class Meta:
        model = Survey
        fields = ('owner', 'name', 'questions')

    def get_questions(self, obj):
        questions = QuestionSerializer(obj.questions.all(), many=True).data
        return questions