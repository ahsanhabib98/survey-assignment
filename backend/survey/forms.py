from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from survey.models import (Answer, Question, Customer, CustomerAnswer, User)


class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        if commit:
            user.save()
        return user


class CustomerSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        Customer.objects.create(user=user)
        return user


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'answer_type',)


class TakeSurveyForm(forms.ModelForm):
    class Meta:
        model = CustomerAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        if self.question.answer_type == 'text-field' or self.question.answer_type  == 'number-field':
            self.fields['answer'] = forms.CharField(
                widget=forms.TextInput(),
                required=True)
        else:
            self.fields['answer'] = forms.ModelChoiceField(
                queryset=self.question.answers.order_by('text'),
                widget=forms.RadioSelect(),
                required=True,
                empty_label=None)
                
    def clean_answer(self):
        answer = self.cleaned_data['answer']
        if type(answer) == str:
            answer = Answer.objects.create(
                text=answer,
                question=self.question
            )
        return answer