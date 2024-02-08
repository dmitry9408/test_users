from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from django.views.generic.base import TemplateView

from .models import AdvUser
from .forms import RegisterForm, ProfileEditForm
from .utilities import signer

# Create your views here.


def index(request):
    users = AdvUser.objects.all()
    context = {'users': users}
    return render(request, 'index.html', context)


def user_detail(request, username):
    user = AdvUser.objects.get(username=username)
    context = {'user': user}
    return render(request, 'user_detail.html', context)


class RegisterView(CreateView):
    model = AdvUser
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'activation_failed.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'activation_done_earlier.html'
    else:
        template = 'activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class UsersLoginView(LoginView):
    template_name = 'login.html'


class UsersLogoutView(LogoutView):
    pass


@login_required
def profile(request):
    user = AdvUser.objects.get(username=request.user.username)
    context = {'user': user}
    return render(request, 'profile.html', context)


class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_edit.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


class PassResetView(PasswordResetView, SuccessMessageMixin):
    template_name = 'password_reset_form.html'
    subject_template_name = 'email/password_reset_subject.txt'
    email_template_name = 'email/password_reset_email.txt'
    success_url = reverse_lazy('main:profile')
    success_message = "Письмо отправлено на почту"


class PassResetConfirmView(PasswordResetConfirmView, SuccessMessageMixin):
    template_name = 'password_reset_confirm.html'
    title = "Введите новый пароль"
    post_reset_login = True
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль успешно обновлен'


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'profile_edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)