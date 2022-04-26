from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from delicious_project.accounts.forms import RegisterForm, LoginForm, ChangePasswordForm, EditProfileForm, \
    ProfileDeleteForm
from delicious_project.accounts.models import Profile

UserModel = get_user_model()


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login_page.html'

    def get_success_url(self):
        return reverse_lazy('home')


class ChangeUserPasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout_page.html'
    next_page = reverse_lazy('home')


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    # full name, photo, age, gender, recipes counter, cooked counter


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/profile_edit.html'


    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('profile details', kwargs={'pk': profile_id})


class ProfileDeleteView(LoginRequiredMixin, CreateView, DeleteView):
    model = Profile
    form_class = ProfileDeleteForm
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('home')

