from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from user import models as user_models

class Application(models.Model):
  app_id = models.UUIDField(
    primary_key = True, 
    default = uuid.uuid4, 
    editable = False
  )
  app_name = models.CharField(max_length = 512)
  app_img_url = models.CharField(max_length = 512)
  def __str__(self):
    return str(self.app_id)

class Subscription(models.Model):
  class SubscriptionTypes(models.TextChoices):
    WEEK = "W", _("week")
    MONTH = "M", _("month")
    YEAR = "Y", _("year")
    LIFE_TIME = "L", _("life_time")
  email = models.ForeignKey(
    user_models.User, 
    on_delete = models.CASCADE, 
    db_column = "email"
  )
  app_id = models.ForeignKey(
    Application, 
    on_delete = models.CASCADE, 
    db_column = "app_id"
  )
  sub_type = models.CharField(
    max_length = 2, 
    choices = SubscriptionTypes.choices,
    default = SubscriptionTypes.MONTH
  )
  bill = models.IntegerField()
  startdate = models.DateField()
  enddate = models.DateField(null = True)
  created_at = models.DateTimeField()
  class Meta:
    unique_together = (("email","app_id"),)
  def __str__(self):
    return str(self.app_id) + "(" + str(self.email) + ")"
  
class Subscription_Bill(models.Model):
  email = models.ForeignKey(
    user_models.User, 
    on_delete = models.CASCADE, 
    db_column = "email"
  )
  app_id = models.ForeignKey(
    Application, 
    on_delete = models.CASCADE, 
    db_column = "app_id"
  )
  week_bill = models.IntegerField()
  month_bill = models.IntegerField()
  year_bill = models.IntegerField()
  class Meta:
    unique_together = (("email","app_id"),)
  def __str__(self):
    return str(self.app_id) + "(" + str(self.email) + ")"
