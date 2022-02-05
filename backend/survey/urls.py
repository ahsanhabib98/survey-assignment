from django.urls import include, path

from .views import survey, customers, admins

urlpatterns = [
    path('', survey.home, name='home'),

    path('customers/', include(([
        path('', customers.SurveyListView.as_view(), name='survey_list'),
        path('taken/', customers.TakenSurveyListView.as_view(), name='taken_survey_list'),
        path('survey/<int:pk>/', customers.take_survey, name='take_survey'),
    ], 'survey'), namespace='customers')),

    path('admins/', include(([
        path('', admins.SurveyListView.as_view(), name='survey_change_list'),
        path('survey/add/', admins.SurveyCreateView.as_view(), name='survey_add'),
        path('survey/<int:pk>/', admins.SurveyUpdateView.as_view(), name='survey_change'),
        path('survey/<int:pk>/results/', admins.SurveyResultsView.as_view(), name='survey_results'),
        path('survey/<int:pk>/question/add/', admins.question_add, name='question_add'),
        path('survey/<int:survey_pk>/question/<int:question_pk>/', admins.question_change, name='question_change'),
    ], 'survey'), namespace='admins')),
]
