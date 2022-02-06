from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    SurveyViewSet, 
    QuestionViewSet,
    AnswerViewSet,
    QuestionAnswerViewSet,
    CustomerAnswerViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'surveys', SurveyViewSet, base_name='surveys')
router.register(r'questions', QuestionViewSet, base_name='questions')
router.register(r'answers', AnswerViewSet, base_name='answers')
router.register(r'question-answers', QuestionAnswerViewSet, base_name='question_answers')
router.register(r'customer-answer', CustomerAnswerViewSet, base_name='customer_answer')

urlpatterns = router.urls