from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserChangeForm,
                                       UserCreationForm)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = \
            "col-10 col-md-4 p-4 mx-auto rounded-4 border border-3 border-primary"
        self.helper.layout = Layout(
            HTML('<h4 class="mb-4">Login</h4>'),
            FloatingField("username"),
            FloatingField("password"),
            Div(Submit("submit", "Submit"), css_class="d-grid m-3"),
            HTML(
                "<a href='{% url 'users:password_reset' %}'>Forgot your password ?</a>"
            ),
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = \
            "col-10 col-md-4 p-4 mx-auto rounded-4 border border-3 border-primary"
        self.helper.layout = Layout(
            FloatingField("email"),
            Div(Submit("submit", "Submit"), css_class="d-grid m-2"),
        )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = \
            "col-10 col-md-4 p-4 mx-auto rounded-4 border border-3 border-primary"
        self.helper.layout = Layout(
            FloatingField("new_password1"),
            FloatingField("new_password2"),
            Div(Submit("submit", "Submit"), css_class="d-grid m-2"),
        )
