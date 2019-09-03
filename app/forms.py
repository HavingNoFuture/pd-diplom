from django import forms
# from django.contrib.auth.models import User
from app.models import User

class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput)
    password_check.label = 'Повторите пароль:'

    password = forms.CharField(widget=forms.PasswordInput)
    password.label = 'Пароль:'
    password.help_text = 'Придумайте пароль.'

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'second_name',
            'email',
            'password',
            'password_check',
            'company',
            'position',
        )

        labels = {
            'first_name': 'Имя:',
            'last_name': 'Фамилия:',
            'second_name': 'Отчество',
            'email': 'Email:',
            'username': 'Логин:',
            'company': 'Компания',
            'position': 'Должность',
        }

        help_texts = {
            'email': 'Пожалуйста, укзаывайте реальный адресс.',
        }

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if password != password_check:
            raise forms.ValidationError('Пароли не совпадают! Попробуйте снова!')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот Email уже занят другим пользователем!')




class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    email.label = 'Email:'
    password.label= 'Пароль:'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такого Email нет в системе!')

        user = User.objects.get(email=email)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')
