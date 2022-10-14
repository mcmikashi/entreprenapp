from core.utils import link_callback
from core.views import (
    CoreCreateView,
    CoreDeleteView,
    CoreDetailView,
    CoreListView,
    CoreUpdateView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import formset_factory, modelformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, View
from xhtml2pdf import pisa

from .forms import (
    CustomerForm,
    EstimateForm,
    ItemForm,
    OrderLineForm,
    OrderLineFormSetHelper,
    OrderLineFormUpdateSetHelper,
    SalerForm,
)
from .models import Customer, Estimate, Item, OrderLine, Saler


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


class EstimateListView(CoreListView):
    model = Estimate
    template_name = "sales/estimate/list.html"


class EstimateDetailView(CoreDetailView):
    model = Estimate
    template_name = "sales/estimate/detail.html"


class EstimateCreateView(LoginRequiredMixin, FormView):
    model = Estimate
    form_class = EstimateForm
    template_name = "sales/estimate/add.html"
    success_url = reverse_lazy("sales:estimate_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        default_formset = formset_factory(
            OrderLineForm, min_num=1, validate_min=True
        )
        context.setdefault("formset", default_formset)
        context["order_lines_helper"] = OrderLineFormSetHelper
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = self.get_context_data()
        formset = context["formset"](request.POST)
        if formset.is_valid() and form.is_valid():
            order_line_instances = []
            for order_line_data in formset.cleaned_data:
                if order_line_data:
                    order_line = OrderLine.objects.create(**order_line_data)
                order_line_instances.append(order_line)
            estimate = Estimate.objects.create(
                **form.cleaned_data,
                created_by=self.request.user,
            )
            estimate.order_lines.set(order_line_instances)
            estimate.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("The estimate was created successfully"),
            )
            return redirect(reverse_lazy("sales:estimate_list"))
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class EstimateUpdateView(LoginRequiredMixin, FormView):
    model = Estimate
    form_class = EstimateForm
    template_name = "sales/estimate/edit.html"
    success_url = reverse_lazy("sales:estimate_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_to_update = get_object_or_404(
            Estimate, pk=self.kwargs.get("pk")
        )
        default_formset = modelformset_factory(
            OrderLine,
            OrderLineForm,
            min_num=1,
            validate_min=True,
            can_delete=True,
        )
        context["default_formset"] = default_formset
        formset = default_formset(queryset=object_to_update.order_lines.all())
        context["object"] = object_to_update
        context["form"] = self.form_class(instance=object_to_update)
        context.setdefault("formset", formset)
        context["order_lines_helper"] = OrderLineFormUpdateSetHelper
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = self.form_class(request.POST, instance=context["object"])
        formset = context["default_formset"](request.POST)
        if formset.is_valid() and form.is_valid():
            estimate = form.save(commit=False)
            formset.save()
            for new_oder_line in formset.new_objects:
                estimate.order_lines.add(new_oder_line)
            estimate.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("The estimate was updated successfully"),
            )
            return redirect(reverse_lazy("sales:estimate_list"))
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class EstimateDeleteView(SuccessMessageMixin, CoreDeleteView):
    model = Estimate
    template_name = "sales/estimate/delete.html"
    success_url = reverse_lazy("sales:estimate_list")


class EstimatePDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if kwargs.get("pk"):
            estimate = get_object_or_404(Estimate, pk=kwargs.get("pk"))
            if not self.request.user.is_superuser and not estimate.is_active:
                return Http404("This page doesn't exist")
        template_path = "sales/estimate/pdf.html"
        context = {"object": estimate}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            "as_attachment=False; "
            f"filename=Estimate n° {estimate.estimate_saler_number:08}"
        )
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback
        )
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")
        return response
