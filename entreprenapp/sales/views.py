from core.views import (
    CoreCreateView,
    CoreDeleteView,
    CoreListView,
    CoreUpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import CustomerForm, ItemForm, SalerForm
from .models import Customer, Item, Saler


class SalerListView(CoreListView):
    model = Saler
    template_name = "sales/saler/list.html"


class SalerCreateView(SuccessMessageMixin, CoreCreateView):
    model = Saler
    form_class = SalerForm
    template_name = "core/default/add.html"
    success_url = reverse_lazy("sales:saler_list")
    success_message = _("%(name)s was created successfully")


class SalerUpdateView(SuccessMessageMixin, CoreUpdateView):
    model = Saler
    form_class = SalerForm
    template_name = "core/default/edit.html"
    success_url = reverse_lazy("sales:saler_list")
    success_message = _("%(name)s was updated successfully")


class SalerDeleteView(CoreDeleteView):
    model = Saler
    template_name = "sales/saler/delete.html"
    success_url = reverse_lazy("sales:saler_list")


class CustomerListView(CoreListView):
    model = Customer
    template_name = "sales/customer/list.html"


class CustomerCreateView(SuccessMessageMixin, CoreCreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "core/default/add.html"
    success_url = reverse_lazy("sales:customer_list")
    success_message = _("%(name)s was created successfully")


class CustomerUpdateView(SuccessMessageMixin, CoreUpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "core/default/edit.html"
    success_url = reverse_lazy("sales:customer_list")
    success_message = _("%(name)s was updated successfully")


class CustomerDeleteView(CoreDeleteView):
    model = Customer
    template_name = "sales/customer/delete.html"
    success_url = reverse_lazy("sales:customer_list")


class ItemListView(CoreListView):
    model = Item
    template_name = "sales/item/list.html"


class ItemCreateView(SuccessMessageMixin, CoreCreateView):
    model = Item
    form_class = ItemForm
    template_name = "core/default/add.html"
    success_url = reverse_lazy("sales:item_list")
    success_message = _("%(label)s was created successfully")


class ItemUpdateView(SuccessMessageMixin, CoreUpdateView):
    model = Item
    form_class = ItemForm
    template_name = "core/default/edit.html"
    success_url = reverse_lazy("sales:item_list")
    success_message = _("%(label)s was updated successfully")


class ItemDeleteView(CoreDeleteView):
    model = Item
    template_name = "sales/item/delete.html"
    success_url = reverse_lazy("sales:item_list")
