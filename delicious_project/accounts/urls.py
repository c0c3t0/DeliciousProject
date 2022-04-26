from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from delicious_project.accounts.views import UserRegisterView, UserLoginView, UserLogoutView, ChangeUserPasswordView, \
    ProfileDetailsView, ProfileEditView, ProfileDeleteView

urlpatterns = [

    path('create-profile/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/<int:pk>/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password-change-done/', RedirectView.as_view(url=reverse_lazy('home')), name='password_change_done'),
    #
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit-profile/<int:pk>/', ProfileEditView.as_view(), name='edit profile'),
    path('delete-profile/<int:pk>/', ProfileDeleteView.as_view(), name='delete profile'),

]
