from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from delicious_project.accounts.views import UserRegisterView, UserLoginView, UserLogoutView, ChangeUserPasswordView, \
    ProfileDetailsView, ProfileEditView, ProfileDeleteView, ActivateAccount
from delicious_project.delicious.views.comments import AddCommentView

urlpatterns = [

    path('create-profile/', UserRegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/<int:pk>/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password-change-done/', RedirectView.as_view(url=reverse_lazy('home')), name='password_change_done'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_complete'),

    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit-profile/<int:pk>/', ProfileEditView.as_view(), name='edit profile'),
    path('delete-profile/<int:pk>/', ProfileDeleteView.as_view(), name='delete profile'),

]

from .signals import *
