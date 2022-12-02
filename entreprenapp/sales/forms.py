from datetime import date

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row, Submit
from dateutil.relativedelta import relativedelta
from django.forms import ModelChoiceField, ModelForm, Select

from .models import Customer, Estimate, Invoice, Item, OrderLine, Saler


class SelectWithTotal(Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SelectWithOptionAttribute(Select):
    """
    Use a dict instead of a string for its label. The 'label' key is expected
    for the actual label, any other keys will be used as HTML attributes on
    the option.
    """

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        # This allows using strings labels as usual
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop("label")
        else:
            opt_attrs = {}
        option_dict = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        for key, val in opt_attrs.items():
            option_dict["attrs"][key] = val
        return option_dict


class ItemChoiceField(ModelChoiceField):
    """ChoiceField with puts data_total attribute on <options>"""

    # Use our custom widget:
    widget = SelectWithOptionAttribute

    def label_from_instance(self, obj):
        # 'obj' will be an Item
        return {
            # the usual label:
            "label": super().label_from_instance(obj),
            # the new data attribute:
            "data-total": obj.including_tax,
            "data-index": obj.pk,
        }


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
        self.fields["quantity"].widget.attrs["min"] = 1
        self.fields["item"].queryset = Item.objects.filter(is_active=True)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("item", css_class="order_line_item")),
                Column(
                    FloatingField("quantity", css_class="order_line_quantity")
                ),
                Column(
                    HTML(
                        "<p class='text-center'>Total : "
                        "<span class='total_line'></span></p>"
                    )
                ),
            )
        )

    class Meta:
        model = OrderLine
        fields = ["item", "quantity"]
        field_classes = {"item": ItemChoiceField}


class OrderLineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Row(
                Column(
                    FloatingField("item", css_class="order_line_item"),
                ),
                Column(
                    FloatingField("quantity", css_class="order_line_quantity")
                ),
                Column(
                    HTML(
                        "<p class='text-center'>Total : "
                        "<span class='total_line'></span></p>"
                    )
                ),
            )
        )


class OrderLineFormUpdateSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Row(
                Column(
                    FloatingField("item", css_class="order_line_item"),
                ),
                Column(
                    FloatingField("quantity", css_class="order_line_quantity")
                ),
                Column(
                    Field(
                        "DELETE",
                        autocomplete="off",
                        template="core/form/custom_delete_checkbox.html",
                        css_class="order_line_item_delete",
                    ),
                    css_class="col-md-1",
                ),
                Column(
                    HTML("<span class='total_line oderline_total'></span>"),
                    css_class="d-none",
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
