from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from delicious_project.accounts.models import Profile

UserModel = get_user_model()


class ProfileTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'pesho@pesh.ov',
        'password': 'pesho_pass',
    }

    def test_profile_create__when_first_name_contain_only_letters__expect_success(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)
        profile = Profile(
            first_name='Pesho',
            last_name='Peshov',
            gender='Male',
            user=user,
        )
        profile.full_clean()
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)

        profile = Profile(
            first_name='Pesh0',
            last_name='Peshov',
            gender='Male',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_random_signs__expect_to_fail(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)

        profile = Profile(
            first_name='Pe%$ho',
            last_name='Peshov',
            gender='Male',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_space__expect_to_fail(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)

        profile = Profile(
            first_name='Pe sho',
            last_name='Peshov',
            gender='Male',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_a_digit__expect_to_fail(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)

        profile = Profile(
            first_name='Pesho',
            last_name='Peshov3',
            gender='Male',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_random_signs__expect_to_fail(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)

        profile = Profile(
            first_name='Pesho',
            last_name='Pe$hov%',
            gender='Male',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_space__expect_to_fail(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)

        profile = Profile(
            first_name='Pesho',
            last_name='Pe shov',
            gender='Male',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)
