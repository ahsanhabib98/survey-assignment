from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admins:survey_change_list')
        else:
            return redirect('customers:survey_list')
    return render(request, 'survey/home.html')
