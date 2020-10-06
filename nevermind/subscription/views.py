from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from .models import *
from user.models import *
from urllib.parse import quote, unquote
from project.config import APIConfig
import json, requests, datetime

APP_LIST_URL = APIConfig['APP_LIST_URL']


def timestamp_to_date(js_timestamp):
  return datetime.datetime.fromtimestamp(int(js_timestamp) / 1000).date()

def calc_subscription_bill(sub_type, bill):
  bill_types = {
    'W': [ 'week_bill', { 'M': 4, 'Y': 52 } ],
    'M': [ 'month_bill', { 'Y': 12 } ],
    'Y': [ 'year_bill', {} ],
  }
  bills = {
    'week_bill': 0,
    'month_bill': 0,
    'year_bill': 0,
  }
  if sub_type == 'L':
    return bills
  bills[bill_types[sub_type][0]] = bill
  for k, v in bill_types[sub_type][1].items():
    bills[bill_types[k][0]] = bill * v
  return bills


@csrf_exempt
def add(req):
  reqobj = {
    'session_id': req.POST.get('session_id'),
    'app_name': req.POST.get('app_name'),
    'app_img_url': req.POST.get('app_img_url'),
    'sub_type': req.POST.get('sub_type'),
    'bill': req.POST.get('bill'),
    'startdate': req.POST.get('startdate'),
    'enddate': req.POST.get('enddate'),
  }
  resobj = {
    'is_add': False,
    'error_msg': None,
  }
  try:
    session = Session.objects.get(
      session_id = reqobj['session_id']
    )
  except Session.DoesNotExist:
    session = None
    resobj['error_msg'] = 'Session does not exist'
    return JsonResponse(resobj)
  user = User.objects.get(email = session.email)

  try:
    app = Application.objects.get(
      app_name = quote(reqobj['app_name'])
    )
  except Application.DoesNotExist:
    app = Application()
    app.app_name = quote(reqobj['app_name'])
    app.app_img_url = reqobj['app_img_url']
    app.save()

  try:
    subscription = Subscription.objects.get(
      email = user.email, app_id = app.app_id
    )
    resobj['error_msg'] = 'Already subscribed'
    return JsonResponse(resobj) 
  except Subscription.DoesNotExist:
    subscription = Subscription()
    subscription.app_id = app
    subscription.email = user

    # TODO: Test sub_type TextChioces .label value later
    subscription.sub_type = reqobj['sub_type'][0:1].upper()

    subscription.bill = int(reqobj['bill'].replace(',', ''))
    subscription.startdate = timestamp_to_date(reqobj['startdate'])
    subscription.enddate = timestamp_to_date(reqobj['enddate'])
    subscription.created_at = timezone.now()
    subscription.save()

  try:
    subscription_bill = Subscription_Bill.objects.get(
      email = user.email, app_id = app.app_id
    )
    resobj['error_msg'] = 'Already subscribed (bill info)'
    return JsonResponse(resobj)
  except Subscription_Bill.DoesNotExist:
    subscription_bill = Subscription_Bill()
    subscription_bill.app_id = app
    subscription_bill.email = user
    sub_bills = calc_subscription_bill(
      reqobj['sub_type'][0:1].upper(),
      int(reqobj['bill'].replace(',', ''))
    )
    subscription_bill.week_bill = sub_bills['week_bill']
    subscription_bill.month_bill = sub_bills['month_bill']
    subscription_bill.year_bill = sub_bills['year_bill']
    subscription_bill.save()

  resobj['is_add'] = True
  return JsonResponse(resobj)


@csrf_exempt
def get(req):
  reqobj = {
    'session_id': req.POST.get('session_id'),
  }
  resobj = {
    'is_get': False,
    'error_msg': None,
    'subscriptions': [],
  }

  try:
    session = Session.objects.get(
      session_id = reqobj['session_id']
    )
  except Session.DoesNotExist:
    reqobj['error_msg'] = 'Session does not exist'
    return JsonResponse(resobj)
  
  qs_subscriptions = Subscription.objects.filter(
    email = session.email
  )

  for sub_info in qs_subscriptions:
    try:
      app = Application.objects.get(app_id = sub_info.app_id.app_id)
      subscription_bill = Subscription_Bill.objects.get(
        email = session.email, app_id = sub_info.app_id
      )
      sub_type_index = sub_info.SubscriptionTypes.values.index(
        sub_info.sub_type
      )
      sub_info_json = {
        'app_id': app.app_id,
        'app_name': unquote(app.app_name),
        'app_img_url': app.app_img_url,
        'sub_type': sub_info.sub_type,
        'sub_type_label': sub_info.SubscriptionTypes.labels[sub_type_index],
        'bill': sub_info.bill,
        'startdate': sub_info.startdate,
        'enddate': sub_info.enddate,
        'week_bill': subscription_bill.week_bill,
        'month_bill': subscription_bill.month_bill,
        'year_bill': subscription_bill.year_bill,
      }
      resobj['subscriptions'].append(sub_info_json)
    except Application.DoesNotExist:
      resobj['error_msg'] = str(app_id) + ' - No such application'
      return JsonResponse(resobj)
  
  resobj['is_get'] = True
  return JsonResponse(resobj)


@csrf_exempt
def update(req):
  reqobj = {
    'session_id': req.POST.get('session_id'),
    'app_id': req.POST.get('app_id'),
    'app_name': req.POST.get('app_name'),
    'app_img_url': req.POST.get('app_img_url'),
    'sub_type': req.POST.get('sub_type'),
    'bill': req.POST.get('bill'),
    'startdate': req.POST.get('startdate'),
    'enddate': req.POST.get('enddate'),
  }
  resobj = {
    'is_update': False,
    'error_msg': None,
  }

  try:
    session = Session.objects.get(session_id = reqobj['session_id'])
    app = Application.objects.get(app_id = reqobj['app_id'])
    subscription = Subscription.objects.get(
      email = session.email, app_id = app.app_id
    )
    subscription_bill = Subscription_Bill.objects.get(
      email = session.email, app_id = app.app_id
    )
    subscription.sub_type = reqobj['sub_type'][0:1].upper()
    subscription.bill = int(reqobj['bill'].replace(',', ''))
    subscription.startdate = timestamp_to_date(reqobj['startdate'])
    subscription.enddate = timestamp_to_date(reqobj['enddate'])
    sub_bills = calc_subscription_bill(
      subscription.sub_type,
      subscription.bill
    )
    subscription_bill.week_bill = sub_bills['week_bill']
    subscription_bill.month_bill = sub_bills['month_bill']
    subscription_bill.year_bill = sub_bills['year_bill']
    subscription.save()
    subscription_bill.save()
  except Session.DoesNotExist:
    resobj['error_msg'] = 'Session does not exist'
    return JsonResponse(resobj)
  except Application.DoesNotExist:
    resobj['error_msg'] = 'Application is not subscribed'
    return JsonResponse(resobj)

  resobj['is_update'] = True
  return JsonResponse(resobj)


@csrf_exempt
def delete(req):
  reqobj = {
    'session_id': req.POST.get('session_id'),
    'app_id': req.POST.get('app_id'),
  }
  resobj = {
    'is_delete': False,
    'error_msg': None,
  }

  try:
    session = Session.objects.get(
      session_id = reqobj['session_id']
    )
    app = Application.objects.get(
      app_id = reqobj['app_id']
    )
    subscription = Subscription.objects.get(
      email = session.email,
      app_id = app.app_id
    )
    subscription_bill = Subscription_Bill.objects.get(
      email = session.email,
      app_id = app.app_id
    )

    # TODO Check constraint for email attribute
    app.delete()
    subscription.delete()
    subscription_bill.delete()
  except Session.DoesNotExist:
    reqobj['error_msg'] = 'Session does not exist'
    return JsonResponse(resobj)
  except Application.DoesNotExist:
    resobj['error_msg'] = 'The application is not subscribed'
    return JsonResponse(resobj)

  resobj['is_delete'] = True
  return JsonResponse(resobj)


def applist(req):
  resobj = {
    'is_applist': False,
    'error_msg': None,
    'applist': None,
  }
  res = requests.get(APP_LIST_URL)
  if res is not None:
    if res.text is not None:
      resobj['is_applist'] = True
      resobj['applist'] = json.loads(res.text)
  else:
    resobj['error_msg'] = 'App List cannot be fetched'
  return JsonResponse(resobj)
