from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

UserModel = get_user_model()


class Test(TestCase):

    def test_login_uses_correct_template(self):
        UserModel.objects.create_user(email='test@test.ov', password='test_pass')
        self.client.login(email='test@test.ov', password='test_pass')
        response = self.client.get(reverse('login'))

        self.assertEqual(str(response.context['user']), 'test@test.ov')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
