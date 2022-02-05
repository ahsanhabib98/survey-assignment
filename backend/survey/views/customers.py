from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from ..decorators import customer_required
from ..forms import CustomerSignUpForm, TakeSurveyForm
from ..models import Survey, Customer, TakenSurvey, User


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customers:survey_list')


@method_decorator([login_required, customer_required], name='dispatch')
class SurveyListView(ListView):
    model = Survey
    ordering = ('name', )
    context_object_name = 'surveyes'
    template_name = 'survey/customers/survey_list.html'

    def get_queryset(self):
        customer = self.request.user.customer
        taken_surveyes = customer.surveyes.values_list('pk', flat=True)
        queryset = Survey.objects.exclude(pk__in=taken_surveyes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, customer_required], name='dispatch')
class TakenSurveyListView(ListView):
    model = TakenSurvey
    context_object_name = 'taken_surveyes'
    template_name = 'survey/customers/taken_survey_list.html'

    def get_queryset(self):
        queryset = self.request.user.customer.taken_surveyes \
            .order_by('survey__name')
        return queryset


@login_required
@customer_required
def take_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    customer = request.user.customer

    if customer.surveyes.filter(pk=pk).exists():
        return render(request, 'customers/taken_survey.html')
    
    total_questions = survey.questions.count()
    unanswered_questions = customer.get_unanswered_questions(survey)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeSurveyForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                customer_answer = form.save(commit=False)
                customer_answer.customer = customer
                customer_answer.save()
                if customer.get_unanswered_questions(survey).exists():
                    return redirect('customers:take_survey', pk)
                else:
                    TakenSurvey.objects.create(customer=customer, survey=survey)
                    return redirect('customers:survey_list')
    else:
        form = TakeSurveyForm(question=question)

    return render(request, 'survey/customers/take_survey_form.html', {
        'survey': survey,
        'question': question,
        'form': form,
        'progress': progress
    })
