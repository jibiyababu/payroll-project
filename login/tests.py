from django.test import TestCase
from django.test import Client
from .forms import *

class Setup_Class(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="test",password="test#123")

        class User_Form_Test(TestCase):

            # Valid Form Data
            def test_UserForm_valid(self):
                form = UserForm(data={'username':'pqabc','password1':'pqabc#123','password2':'pqabc#123'})
                self.assertTrue(form.is_valid())
                print(assertTrue(form.is_valid()))

            # Invalid Form Data
            def test_UserForm_invalid(self):
                form = UserForm(data={'username':'abc','password1':'abc#123','password2':'abc#123'})
                self.assertFalse(form.is_valid())

