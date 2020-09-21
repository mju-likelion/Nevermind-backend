from django.shortcuts import render
from django.http import JsonResponse
import json
import requests

APP_LIST_URL = 'https://rss.itunes.apple.com/api/v1/kr/ios-apps/top-free/all/100/explicit.json'


def add(req):
  #
  return JsonResponse({})


def get(req):
  #
  return JsonResponse({})


def update(req):
  #
  return JsonResponse({})


def delete(req):
  #
  return JsonResponse({})


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
