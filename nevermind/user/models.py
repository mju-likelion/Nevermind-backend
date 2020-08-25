from django.db import models

class User(models.Model):
  email = models.EmailField(max_length = 50, primary_key = True)
  pwd = models.CharField(max_length = 20)
  username = models.CharField(max_length = 50)
  cellphone = models.CharField(max_length = 20)
  created_at = models.DateTimeField()
  def __str__(self):
    return self.email

class Session(models.Model):
  session_id = models.CharField(max_length = 50, primary_key = True);
  email = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'email')
  ip_address = models.CharField(max_length = 45)
  def __str__(self):
    return self.email
