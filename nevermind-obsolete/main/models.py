from django.db import models

class User(models.Model):
  email = models.EmailField(max_length = 50, primary_key = True)
  pwd = models.CharField(max_length = 20)
  name = models.CharField(max_length = 50)
  cell_phone = models.CharField(max_length = 20)
  created_at = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.email
