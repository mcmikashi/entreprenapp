from decimal import Decimal

from core.models import Core
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class SalesActorBase(Core):
    name = models.CharField(_("name"), max_length=200)
    adress = models.CharField(_("adress"), max_length=254)
    city = models.CharField(_("city"), max_length=100)
    postal_code = models.CharField(_("postal_code"), max_length=15)
    country = CountryField(blank=True)
    email = models.EmailField(_("email address"), max_length=254, blank=True)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ["name"]


class Saler(SalesActorBase):
    logo = models.ImageField(
        _("logo"),
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True,
    )
    estimate_number = models.IntegerField(
        ("estimate number"), default=0, editable=False
    )
    invoice_number = models.IntegerField(
        ("invoice number"), default=0, editable=False
    )

    class Meta(SalesActorBase.Meta):
        verbose_name = _("Saler")
        verbose_name_plural = _("Salers")


class Customer(SalesActorBase):
    class Meta(SalesActorBase.Meta):
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class Item(Core):
    label = models.CharField(_("label"), max_length=254)
    description = models.TextField(_("description"), blank=True)
    price_duty_free = models.DecimalField(
        _("price"), max_digits=10, decimal_places=2
    )
    tax = models.DecimalField(_("tax"), max_digits=5, decimal_places=2)

    @property
    def tax_price(self) -> Decimal:
        "Return the price tax of the item."
        return Decimal(self.price_duty_free * (self.tax / 100))

    @property
    def including_tax(self) -> Decimal:
        "Return the including tax of the transaction."
        return Decimal(self.price_duty_free + self.tax_price)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ["label"]
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class OrderLine(Core):
    item = models.ForeignKey(
        "sales.Item", verbose_name=_("item"), on_delete=models.CASCADE
    )
    quantity = models.IntegerField(_("quantity"))

    @property
    def subtotal_duty_free(self) -> Decimal:
        "Return the price (duty free) of the oderline."
        return Decimal(self.item.price_duty_free * self.quantity)

    @property
    def subtotal_tax_price(self) -> Decimal:
        "Return tax price of the oderline."
        return Decimal(self.item.tax_price * self.quantity)

    @property
    def subtotal_including_tax(self) -> Decimal:
        "Return price (including tax) of the oderline."
        return Decimal(self.item.including_tax * self.quantity)

    def __str__(self):
        return f"{self.item} - {self.quantity}"

    class Meta:
        verbose_name = _("OrderLine")
        verbose_name_plural = _("OrderLines")


class SalesActionBase(Core):
    saler = models.ForeignKey(
        "sales.Saler", verbose_name=_("saler"), on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        "sales.Customer", verbose_name=_("customer"), on_delete=models.CASCADE
    )
    order_lines = models.ManyToManyField(
        "sales.OrderLine", verbose_name=_("order line")
    )
    date = models.DateField(_("date"))

    @property
    def total_price_duty_free(self) -> Decimal:
        "Return the total price (duty free) of the oderline."
        return Decimal(
            sum(
                order_line.subtotal_duty_free
                for order_line in self.order_lines.all()
            )
        )

    @property
    def total_tax_price(self) -> Decimal:
        "Return the total price (including tax) of the oderline."
        return Decimal(
            sum(
                order_line.subtotal_including_tax
                for order_line in self.order_lines.all()
            )
        )

    @property
    def total_price_including_tax(self) -> Decimal:
        "Return the total price (including tax) of the oderline."
        return Decimal(
            sum(
                order_line.subtotal_including_tax
                for order_line in self.order_lines.all()
            )
        )

    def __str__(self):
        return f"{self.saler} - {self.customer} - {self.date}"

    class Meta:
        abstract = True
        ordering = ["modified_date", "id"]


class Estimate(SalesActionBase):
    estimate_saler_number = models.IntegerField(
        _("invoice saler number"), editable=False
    )
    validity_date = models.DateField(_("validity date"))

    def turn_into_an_invoice(self):
        # coppy the data to create an invoice
        order_lines_to_copy = self.order_lines.all()
        new_invoice = Invoice.objects.create(
            saler=self.saler,
            customer=self.customer,
            date=timezone.now(),
            is_paid=False,
        )
        new_invoice.order_lines.set(order_lines_to_copy)
        new_invoice.save()
        return True

    def save(self, *args, **kwargs):
        if not self.estimate_saler_number:
            self.estimate_saler_number = self.saler.estimate_number + 1
            self.saler.estimate_number += 1
            self.saler.save()
        super().save(*args, **kwargs)

    class Meta(SalesActionBase.Meta):
        pass


class Invoice(SalesActionBase):
    invoice_saler_number = models.IntegerField(
        _("invoice saler number"), editable=False
    )
    is_paid = models.BooleanField(_("is paid"))

    def save(self, *args, **kwargs):
        if not self.invoice_saler_number:
            self.invoice_saler_number = self.saler.invoice_number + 1
            self.saler.invoice_number += 1
            self.saler.save()
        super().save(*args, **kwargs)

    class Meta(SalesActionBase.Meta):
        pass
