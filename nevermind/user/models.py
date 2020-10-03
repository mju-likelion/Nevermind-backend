from django.db import models

class User(models.Model):
  email = models.EmailField(max_length = 64, primary_key = True)
  pwd = models.CharField(max_length = 128)
  username = models.CharField(max_length = 128)
  cellphone = models.CharField(max_length = 32)
  created_at = models.DateTimeField()
  def __str__(self):
    return self.email

class Session(models.Model):
  session_id = models.CharField(max_length = 128, primary_key = True);
  email = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'email')
  ip_address = models.CharField(max_length = 45)
  def __str__(self):
    return self.email

class EmailAuthInfo(models.Model):
  email = models.EmailField(max_length = 64)
  authnum = models.CharField(max_length = 8)
  def __str__(self):
    return self.email
