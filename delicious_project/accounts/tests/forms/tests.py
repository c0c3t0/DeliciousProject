from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from delicious_project.accounts.forms import LoginForm, RegisterForm, ChangePasswordForm, EditProfileForm, \
    ProfileDeleteForm
from delicious_project.accounts.models import Profile

UserModel = get_user_model()


class AccountFormsTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@test.ov',
        'password': 'test_pass',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Testov',
        'picture': 'https://photo.jpg',
        'gender': 'Male',
        'date_of_birth': '1991-04-04'
    }

    def test_create_an_empty_login_form(self):
        form = LoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('class="form-control"', form.as_p())

    def test_create_an_empty_register_form(self):
        form = RegisterForm()
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        self.assertIn('gender', form.fields)
        self.assertIn('picture', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('date_of_birth', form.fields)
        self.assertIn('class="form-control"', form.as_p())

    def test_create_an_empty_change_password_form(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        form = ChangePasswordForm(user=user)
        self.assertIn('old_password', form.fields)
        self.assertIn('new_password1', form.fields)
        self.assertIn('new_password2', form.fields)

    def test_create_an_empty_edit_profile_form(self):
        form = EditProfileForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('gender', form.fields)
        self.assertIn('picture', form.fields)
        self.assertIn('date_of_birth', form.fields)

    def test_edit_form_receives_valid_data__expect_success(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)

        form_data = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'gender': profile.gender,
            'picture': profile.picture,
            'date_of_birth': profile.date_of_birth,
        }
        form = EditProfileForm(data=form_data)
        form.instance.user = user

        self.assertTrue(form.is_valid())
        obj = form.save()
        self.assertEqual(obj.first_name, profile.first_name)
        self.assertEqual(obj.last_name, profile.last_name)
        self.assertEqual(obj.gender, profile.gender)
        self.assertEqual(obj.picture, profile.picture)
        self.assertEqual('1991-04-04', profile.date_of_birth)

    def test_edit_form_receives_invalid_data__expect_to_fail(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.first_name = 'Te$t'

        form_data = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'gender': profile.gender,
            'picture': profile.picture,
            'date_of_birth': profile.date_of_birth,
        }
        form = EditProfileForm(data=form_data)
        form.instance.user = user

        self.assertFalse(form.is_valid())

    def test_create_delete_form(self):
        form = ProfileDeleteForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('gender', form.fields)
        self.assertIn('picture', form.fields)
        self.assertIn('date_of_birth', form.fields)

    def test_delete_form_receives_valid_data__expect_success(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)

        form = ProfileDeleteForm()
        form.instance.user = user

        self.client.get(reverse('delete profile', args=(profile.pk,)), follow=True)
        self.assertTemplateUsed('auth/profile_delete.html')
