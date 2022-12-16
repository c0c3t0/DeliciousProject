from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm

from django import forms
from django.core.validators import MinLengthValidator
from django.forms import EmailField

from delicious_project.accounts.models import Profile
from delicious_project.common.helpers import DisabledFieldsFormMixin
from delicious_project.common.validators import contain_only_letters_validator, a_hundred_years_ago, yesterday
from delicious_project.delicious.models import Comment

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(Profile.FIRST_NAME_MIN_LENGTH),
            contain_only_letters_validator,
        ),
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
        validators=(
            MinLengthValidator(Profile.LAST_NAME_MIN_LENGTH),
            contain_only_letters_validator,
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
            }
        ),
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
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL',
                # 'required': False,
                # 'blank': True,
                # 'null': True,
            }
        )
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': a_hundred_years_ago(),
                'max': yesterday(),
            }
        )
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
        model = UserModel
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'picture', 'date_of_birth')
        field_classes = {"email": EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Repeat password"
        self.initial['gender'] = "Do not show"
        self.fields['picture'].required = False
        self.fields['date_of_birth'].required = False


class LoginForm(AuthenticationForm):
    username = EmailField(
        label='Email',
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
        fields = ('email', 'password')
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

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Repeat password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['placeholder'] = 'Old password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Repeat password'

class MyPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password"
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Repeat password'

class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': a_hundred_years_ago(),
                'max': yesterday(),
            }
        )
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'gender', 'picture', 'date_of_birth')


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
