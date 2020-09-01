from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from argon2 import PasswordHasher
from urllib.parse import quote, unquote
from .models import User, Session
import json, random


@csrf_exempt
def issession(req):
  reqobj = {
    'session_id': req.POST.get('session_id'),
  }
  resobj = {
    'is_session': False,
    'error_msg': None,
  }
  for key, value in reqobj.items():
    if value is None or value == '':
      resobj['is_session'] = False
      resobj['error_msg'] = 'No session_id sent'
      return JsonResponse(resobj)
  if req.method == 'POST':
    try:
      Session.objects.get(
        session_id = reqobj['session_id']
      )
      resobj['is_session'] = True
    except Session.DoesNotExist:
      resobj['error_msg'] = 'No session exists'
      return JsonResponse(resobj)
  else:
    resobj['error_msg'] = 'Not POST method'
  return JsonResponse(resobj)

@csrf_exempt
def login(req):
  reqobj = {
    'email': req.POST.get('email'),
    'pwd': req.POST.get('pwd'),
  }
  resobj = {
    'is_login': True,
    'username': None,
    'email': None,
    'error_msg': None,
    'session_id': None,
  }
  for key, value in reqobj.items():
    if value is None or value == '':
      resobj['is_login'] = False
      resobj['error_msg'] = 'Both email/password must be sent'
      return JsonResponse(resobj)
  if req.method == 'POST':
    try:
      user = User.objects.get(
        email = reqobj['email']
      )
      user_pw = user.pwd
    except User.DoesNotExist:
      resobj['is_login'] = False
      resobj['error_msg'] = 'User None'
      return JsonResponse(resobj)

    try:
      ph = PasswordHasher()
      ph.verify(user_pw.encode(), reqobj['pwd'].encode())
    except:
      resobj['is_login'] = False
      resobj['error_msg'] = 'Wrong Password'
      return JsonResponse(resobj)

    resobj['email'] = user.email
    resobj['username'] = unquote(user.username)

    try:
      session = Session.objects.get(
        email = reqobj['email']
      )
    except Session.DoesNotExist:
      session = None

    if session is not None:
      if session.ip_address != req.META['REMOTE_ADDR']:
        session.delete()
        session = None

    if session is None:
      session = Session()
      session.session_id = ''.join(
        random.choice(
          '0123456789'
        + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        + 'abcdefghijklmnopqrstuvwxyz'
        + '^%$#@!.,-=+()*&~/<>|;:[]_?'
        ) for i in range(50)
      )
      session.email = user
      session.ip_address = req.META['REMOTE_ADDR']
      session.save()

    resobj['session_id'] = session.session_id

  else: # POST
    resobj['is_login'] = False
    resobj['error_msg'] = 'Not POST method'
    return JsonResponse(resobj)

  response = JsonResponse(resobj)
  response.set_cookie('session_id', resobj['session_id'])
  return response


@csrf_exempt
def logout(req):
  reqobj = {
    'session_id': req.POST.get('session_id'),
  }
  resobj = {
    'is_logout': True,
    'error_msg': None,
  }
  for key, value in reqobj.items():
    if value is None or value == '':
      resobj['is_logout'] = False
      resobj['error_msg'] = 'No session_id sent'
      return JsonResponse(resobj)
  if req.method == 'POST':
    try:
      session = Session.objects.get(
        session_id = reqobj['session_id']
      )
    except Session.DoesNotExist:
      session = None
    if session is not None:
      session.delete()
    else: # Session None
      resobj['is_logout'] = False
      resobj['error_msg'] = 'Session None';
  else: # POST
    resobj['is_logout'] = False
    resobj['error_msg'] = 'Not POST method';
  return JsonResponse(resobj)


@csrf_exempt
def register(req):
  reqobj = {
    'email': req.POST.get('email'),
    'pwd': req.POST.get('pwd'),
    'username': req.POST.get('username'),
    'cellphone': req.POST.get('cellphone'),
  }
  resobj = {
    'is_register': True,
    'created_at': None,
    'error_msg': None,
  }
  for key, value in reqobj.items():
    if value is None or value == '':
      resobj['is_register'] = False
      resobj['error_msg'] = 'Must fill out all inputs in the form'
      return JsonResponse(resobj)
  if req.method == 'POST':
    user = User()
    user.email = reqobj['email']

    ph = PasswordHasher()
    user.pwd = ph.hash(reqobj['pwd'])

    user.username = quote(reqobj['username'])
    user.cellphone = reqobj['cellphone']
    user.created_at = timezone.now()
    user.save()
    resobj['created_at'] = user.created_at
  else:
    resobj['is_register'] = False
    resobj['error_msg'] = 'Not POST method'
  return JsonResponse(resobj)


@csrf_exempt
def unregister(req):
  reqobj = {
    'session_id': req.POST.get('session_id'),
  }
  resobj = {
    'is_unregister': True,
    'email': None,
    'username': None,
    'error_msg': None,
  }
  for key, value in reqobj.items():
    if value is None or value == '':
      resobj['is_unregister'] = False
      resobj['error_msg'] = 'No session_id sent'
      return JsonResponse(resobj)
  if req.method == 'POST':
    try:
      session = Session.objects.get(
        session_id = reqobj['session_id']
      )
    except Session.DoesNotExist:
      session = None
    if session is not None:
      try:
        user = User.objects.get(email = session.email)
      except User.DoesNotExist:
        user = None
      if user is not None:
        resobj['email'] = user.email
        resobj['username'] = unquote(user.username)
        session.delete()
        user.delete()
      else: # User None
        resobj['is_unregister'] = False
        resobj['error_msg'] = 'User None'
    else: # Session None
      resobj['is_unregister'] = False
      resobj['error_msg'] = 'Session None'
  else: # Not POST
    resobj['is_unregister'] = False;
    resobj['error_msg'] = 'Not POST method'
  return JsonResponse(resobj)
