# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
import secrets
# Django libs
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
# Own libs
from .exceptions import ExistingUserEmailException
from .forms import LoginForm, SignupForm
from .models import EmailToken
from .utils import create_user


# Create your views here.
class SignUp(FormView):
    template_name = 'account/sign-up.html'
    form_class = SignupForm
    success_url = reverse_lazy('account:sign_up_success')

    def form_valid(self, form):
        with transaction.atomic():
            try:
                user = create_user(form.cleaned_data)
                token = EmailToken.objects.create(
                    token=secrets.token_urlsafe(20),
                    user=user
                )
                token.send_confirmation_email()
            except ExistingUserEmailException:
                form.add_error('email', 'El email ya se encuentra registrado')
                return super(SignUp, self).form_invalid(form)
            else:
                return super(SignUp, self).form_valid(form)


sign_up = SignUp.as_view()


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard:index')
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and \
                self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    'Redirection loop for authenticated user detected. '
                    'Check that your LOGIN_REDIRECT_URL doesnt point to '
                    'a login page.'
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = self.request.POST['email']
        password = self.request.POST['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            form.add_error(None, 'Credenciales inválidas')
            return super(LoginView, self).form_invalid(form)
        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            form.add_error(None, 'Credenciales inválidas')
            return super(LoginView, self).form_invalid(form)
        return super(LoginView, self).form_valid(form)


login_view = LoginView.as_view()


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('account:login'))

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('account:login'))


logout_view = LogoutView.as_view()


class VerifyEmailView(View):
    template_name = 'account/email_verified_success.html'

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            email_token = EmailToken.objects.get(token=token)
            email_token.verified = True
            email_token.save()
            return render(request, self.template_name)
        except EmailToken.DoesNotExist:
            return HttpResponseNotFound()


verify_email = VerifyEmailView.as_view()


class EmailUnverified(View):
    template_name = 'account/email_unverified.html'

    def get(self, request, *args, **kwargs):
        if not request.user.emailtoken.verified:
            return render(request, self.template_name)
        return HttpResponseNotFound()

    def post(self, request):
        if not request.user.emailtoken.verified:
            request.user.emailtoken.send_confirmation_email()
            return render(request, 'account/email_resent.html')
        return HttpResponseNotFound()


email_unverified = login_required(EmailUnverified.as_view())
