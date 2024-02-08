from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .signals import post_register
from .models import AdvUser


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput, help_text="Введите пароль еще раз")
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        post_register.send(RegisterForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес эл.почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name')
