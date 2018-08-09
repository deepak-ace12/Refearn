# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from refearn.models import Customer


# Disallow Django self-referential foreign key to point to self object
class CustomerAdmin(admin.ModelAdmin):
    def change_view(self, request, customer_id, form_url='', extra_context=None):
        self.customer_id = customer_id
        return super(CustomerAdmin, self).change_view(
            request, customer_id, form_url, extra_context=extra_context,
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "referral_id":
            kwargs['queryset'] = Customer.objects.exclude(referral_id=self.customer_id)
        return super(CustomerAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

admin.site.register(Customer)


# Register your models here.
