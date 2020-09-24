from django.contrib import admin
from .models import (
  Application, 
  Subscription, 
  Subscription_Bill
)

admin.site.register(Application)
admin.site.register(Subscription)
admin.site.register(Subscription_Bill)
