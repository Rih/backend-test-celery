from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from account import views

app_name = 'account'

urlpatterns = [
    path('/sign-up', views.sign_up, name='sign_up'),
    path('/login', views.login_view, name='login'),
    path('/logout', views.logout_view, name='logout'),
    path('/email-unverified', views.email_unverified, name='email_unverified'),
    path('/verify-email/<str:token>', views.verify_email, name='verify_email'),
    path(
        '/reset-password',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('account:password_reset_done')
        ),
        name='reset_password'
    ),
    path(
        '/password_reset/done',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        '/reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('account:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        '/reset/done',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        '/sign-up/success',
        TemplateView.as_view(template_name='account/sign_up_success.html'),
        name='sign_up_success'
    )

]
