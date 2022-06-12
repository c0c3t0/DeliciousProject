from datetime import date, timedelta, datetime

# from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from django import forms
from django.forms import EmailField

from delicious_project.accounts.models import Profile
from delicious_project.common.helpers import DisabledFieldsFormMixin
from delicious_project.delicious.models import Comment

UserModel = get_user_model()


def yesterday():
    yesterday = date.today() - timedelta(days=1)
    return yesterday


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        widget=forms.TextInput(
            attrs={
                'label': "",
                'class': 'form-control',
                'placeholder': 'First name',
            }
        )
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
            }
        )
    )
    gender = forms.CharField(
        max_length=max(len(x) for x, _ in Profile.GENDERS),
        widget=forms.Select(
            choices=Profile.GENDERS,
            attrs={
                'class': 'form-control',
                'placeholder': 'Gender',
                # 'default': 'Do not show',
            }
        )
    )
    picture = forms.URLField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL',
            }
        )
    )

    date_of_birth = forms.DateField(
        initial=yesterday(),
        # widget=DatePickerInput(),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form',
                'placeholder': 'Email',
            }
        ),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password again',
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'picture', 'date_of_birth')
        field_classes = {"email": EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Repeat password"
        self.initial['gender'] = "Do not show"
        self.fields['picture'].required = False

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            gender=self.cleaned_data['gender'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            user=user,
        )

        if commit:
            profile.save()
        return user


class LoginForm(AuthenticationForm):
    username = EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )

    class Meta:
        model = UserModel
        fields = ('password')
        field_classes = {"email": EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'autofocus': True
            }
        ),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['placeholder'] = 'Old password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'New password again'


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'gender', 'picture', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(datetime.now().year, 1919, -1),

            ), }


class ProfileDeleteForm(DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()

    class Meta:
        model = Profile
        exclude = ('user',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'placeholder': 'Your comment',
                }
            ),
        }
