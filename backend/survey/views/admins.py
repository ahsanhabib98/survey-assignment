from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DetailView, ListView, UpdateView)

from ..decorators import admin_required
from ..forms import QuestionForm, AdminSignUpForm
from ..models import Answer, Question, Survey, User


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('admins:survey_change_list')


@method_decorator([login_required, admin_required], name='dispatch')
class SurveyListView(ListView):
    model = Survey
    ordering = ('name', )
    context_object_name = 'surveyes'
    template_name = 'survey/admins/survey_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.surveyes \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_surveyes', distinct=True))
        return queryset


@method_decorator([login_required, admin_required], name='dispatch')
class SurveyCreateView(CreateView):
    model = Survey
    fields = ('name', )
    template_name = 'survey/admins/survey_add_form.html'

    def form_valid(self, form):
        survey = form.save(commit=False)
        survey.owner = self.request.user
        survey.save()
        messages.success(self.request, 'The survey was created with success! Go ahead and add some questions now.')
        return redirect('admins:survey_change', survey.pk)


@method_decorator([login_required, admin_required], name='dispatch')
class SurveyUpdateView(UpdateView):
    model = Survey
    fields = ('name', )
    context_object_name = 'survey'
    template_name = 'survey/admins/survey_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing surveyes that belongs
        to the logged in user.
        '''
        return self.request.user.surveyes.all()

    def get_success_url(self):
        return reverse('admins:survey_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, admin_required], name='dispatch')
class SurveyResultsView(DetailView):
    model = Survey
    context_object_name = 'survey'
    template_name = 'survey/admins/survey_results.html'

    def get_context_data(self, **kwargs):
        survey = self.get_object()
        taken_surveyes = survey.taken_surveyes.select_related('customer__user').order_by('-date')
        total_taken_surveyes = taken_surveyes.count()
        extra_context = {
            'taken_surveyes': taken_surveyes,
            'total_taken_surveyes': total_taken_surveyes,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.surveyes.all()


@login_required
@admin_required
def question_add(request, pk):
    # By filtering the survey by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # survey will be able to add questions to it.
    survey = get_object_or_404(Survey, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('admins:question_change', survey.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'survey/admins/question_add_form.html', {'survey': survey, 'form': form})


@login_required
@admin_required
def question_change(request, survey_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `survey` and
    # `question` we are making sure only the owner of the survey can
    # change its details and also only questions that belongs to this
    # specific survey can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    survey = get_object_or_404(Survey, pk=survey_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, survey=survey)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        fields=('text',),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('admins:survey_change', survey.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'survey/admins/question_change_form.html', {
        'survey': survey,
        'question': question,
        'form': form,
        'formset': formset
    })