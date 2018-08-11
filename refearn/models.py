# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=40, unique=True)
    referral_id = models.ForeignKey('self',null=True, blank=True)
    payback = models.FloatField(default=0)
    is_ambassador = models.BooleanField(default=False)
    joining_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.email
