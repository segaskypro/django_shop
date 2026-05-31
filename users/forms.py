from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    Использует email как основной идентификатор.
    """
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        help_texts = {
            'username': 'Обязательное поле. Не более 150 символов.',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации пользователя по email и паролю.
    """
    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'phone_number', 'country']