from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView

from delicious_project.accounts.forms import RegisterForm, LoginForm, ChangePasswordForm, EditProfileForm, \
    ProfileDeleteForm
from delicious_project.accounts.models import Profile
from delicious_project.accounts.tokens import account_activation_token
from delicious_project.delicious.models import Recipe

UserModel = get_user_model()


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form,
            'messages': messages.get_messages(request),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            profile = Profile(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                gender=form.cleaned_data['gender'],
                picture=form.cleaned_data['picture'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                user=user,
            )
            profile.save()

            return redirect('login')

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, '
                                       'possibly because it has already been used.'))
            return redirect('home')


class ChangeUserPasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'auth/change_password.html'


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    # def form_valid(self, form):
    #     remember_me = form.cleaned_data.get('remember_me')
    #
    #     if not remember_me:
    #         # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
    #         self.request.session.set_expiry(0)
    #
    #         # Set session as modified to force data updates/cookie to be saved.
    #         self.request.session.modified = True
    #
    #     # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
    #     return super(CustomLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    template_name = 'auth/logout_page.html'
    next_page = reverse_lazy('home')


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_recipes = Recipe.objects.filter(user_id=self.request.user)
        user_recipes_counter = len(user_recipes)
        user_recipes_total_cooks = sum(recipe.cooked_counter for recipe in user_recipes)

        cooked_recipes_by_user = Recipe.objects.filter(cooked=self.request.user).count()

        context.update({
            'user_recipes_counter': user_recipes_counter,
            'user_recipes_total_cooks': user_recipes_total_cooks,
            'cooked_recipes_by_user': cooked_recipes_by_user,
            'is_owner': self.object.user == self.request.user,
            'is_anonymous': not self.request.user.is_authenticated,
        })

        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'profile/profile_edit.html'

    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('profile details', kwargs={'pk': profile_id})


class ProfileDeleteView(LoginRequiredMixin, CreateView, DeleteView):
    model = Profile
    form_class = ProfileDeleteForm
    template_name = 'profile/profile_delete.html'
    success_url = reverse_lazy('home')
