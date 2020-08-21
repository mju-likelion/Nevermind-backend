from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
import json

def main(req):
  users = User.objects
  return render(req, 'main.html', { 'users': users })

def signup(req):
  user = User()
  user.email = req.POST['email']
  user.pwd = req.POST['pwd']
  user.name = req.POST['name']
  user.cell_phone = req.POST['cell_phone']
  user.save()
  return redirect('main')

def deluser(req):
  user = User.objects.get(email = req.POST['email'])
  notif_str = 'User ' + user.name + '(' + user.email + ') has been deleted'
  user.delete()
  context = { 'message': 'User ' + user.name + ' deleted successfully' }
  return HttpResponse(json.dumps(context), content_type = 'application/json')