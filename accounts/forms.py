# accounts/forms.py
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
        "email",
        "username",
        )
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
        "email",
        "username",
        )


# For allauth, to skip password instrucitons
class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts from password fields
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''