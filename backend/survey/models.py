from django.contrib.auth.models import AbstractUser
from django.db import models


ANSWER_TYPE = (
    ('text-field', 'Text Field'),
    ('number-field', 'Number Field'),
    ('dropdown', 'Dropdown'),
    ('checkbox', 'Checkbox'),
    ('radio-button', 'Radio Button'),
)


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Survey(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveyes')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    answer_type = models.CharField(choices=ANSWER_TYPE, max_length=50, null=True, blank=True)
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)

    def __str__(self):
        return self.text


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    surveyes = models.ManyToManyField(Survey, through='TakenSurvey')

    def get_unanswered_questions(self, survey):
        answered_questions = self.survey_answers \
            .filter(answer__question__survey=survey) \
            .values_list('answer__question__pk', flat=True)
        questions = survey.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenSurvey(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='taken_surveyes')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='taken_surveyes')
    date = models.DateTimeField(auto_now_add=True)


class CustomerAnswer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='survey_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
