from datetime import date

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row, Submit
from dateutil.relativedelta import relativedelta
from django.forms import ModelForm

from .models import Customer, Estimate, Invoice, Item, OrderLine, Saler


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


class ItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "col-11 col-md-8 mx-auto"
        self.helper.layout = Layout(
            FloatingField("label"),
            FloatingField("description", css_class="floating-textarea"),
            FloatingField("price_duty_free"),
            FloatingField("tax"),
            Div(Submit("submit", "Submit"), css_class="d-grid m-3"),
        )

    class Meta:
        model = Item
        fields = [
            "label",
            "description",
            "price_duty_free",
            "tax",
        ]


class OrderLineForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("item")),
                Column(FloatingField("quantity")),
            )
        )

    class Meta:
        model = OrderLine
        fields = ["item", "quantity"]


class OrderLineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Row(
                Column(
                    FloatingField("item"),
                ),
                Column(FloatingField("quantity")),
            )
        )


class OrderLineFormUpdateSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Row(
                Column(
                    FloatingField("item"),
                ),
                Column(FloatingField("quantity")),
                Column(
                    Field(
                        "DELETE",
                        autocomplete="off",
                        template="core/form/custom_delete_checkbox.html",
                    ),
                    css_class="col-md-1",
                ),
            )
        )


class EstimateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = date.today()
        self.fields["validity_date"].initial = date.today() + relativedelta(
            days=30
        )
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("saler")),
                Column(FloatingField("customer")),
            ),
            Row(
                Column(FloatingField("date")),
                Column(FloatingField("validity_date")),
            ),
        )

    class Meta:
        model = Estimate
        fields = ["saler", "customer", "date", "validity_date"]


class InvoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = date.today()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("saler")),
                Column(FloatingField("customer")),
            ),
            Row(
                Column(FloatingField("date")),
                Column(Field("is_paid")),
            ),
        )

    class Meta:
        model = Invoice
        fields = ["saler", "customer", "date", "is_paid"]
