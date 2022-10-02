from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django.forms import ModelForm

from .models import Customer, Saler


class SalerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "col-11 col-md-8 mx-auto"
        self.helper.layout = Layout(
            FloatingField("name"),
            FloatingField("adress"),
            FloatingField("city"),
            FloatingField("postal_code"),
            FloatingField("country"),
            FloatingField("email"),
            FloatingField("phone_number"),
            Field("logo"),
            Div(Submit("submit", "Submit"), css_class="d-grid m-3"),
        )

    class Meta:
        model = Saler
        fields = [
            "name",
            "adress",
            "city",
            "postal_code",
            "country",
            "email",
            "phone_number",
            "logo",
        ]


class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "col-11 col-md-8 mx-auto"
        self.helper.layout = Layout(
            FloatingField("name"),
            FloatingField("adress"),
            FloatingField("city"),
            FloatingField("postal_code"),
            FloatingField("country"),
            FloatingField("email"),
            FloatingField("phone_number"),
            Div(Submit("submit", "Submit"), css_class="d-grid m-3"),
        )

    class Meta:
        model = Customer
        fields = [
            "name",
            "adress",
            "city",
            "postal_code",
            "country",
            "email",
            "phone_number",
        ]
