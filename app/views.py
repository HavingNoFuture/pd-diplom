from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm

from app.models import User
from django.contrib.auth.models import User


# Create your views here.
def main_page_view(request):
    return render(request, 'app/main.html')


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    context = {}
    context['form'] = form
    if form.is_valid():
        new_user = form.save(commit=False)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        new_user.set_password(password)
        new_user.first_name = form.cleaned_data['first_name']
        new_user.last_name = form.cleaned_data['last_name']
        new_user.email = email
        new_user.company = form.cleaned_data['company']
        new_user.position = form.cleaned_data['position']
        new_user.second_name = form.cleaned_data['second_name']
        new_user.save()

        login_user = authenticate(email=email, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('main_page'))
        return HttpResponseRedirect(reverse('main_page'))

    return render(request, 'app/registration.html', context)




def login_view(request):
    form = LoginForm(request.POST or None)
    context = {}
    context['form'] = form

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        # email = User.objects.get(email=email).email

        login_user = authenticate(email=email, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('main_page'))

    return render(request, 'app/login.html', context)
