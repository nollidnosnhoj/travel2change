from django.test import TestCase
from django.contrib.auth import get_user_model

class UserManagerTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='test@gmail.com', first_name="test", last_name="user", password="foo")
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@gmail.com", first_name="Super", last_name="User", password="bar", is_superuser = False
            )
