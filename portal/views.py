# This Python file uses the following encoding in format utf-8
import functools
import operator
import random
import unicodedata
import datetime


from django.template.loader import get_template, render_to_string
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from django.db.models import Count
#from rest_framework.permissions import IsAdminUser
from django.shortcuts import redirect

from portal.models import Subscribe
#from portal.utils import SendSubscribeMail, round_next_down, round_next_up
from portal.models import Subscribe

from el_pagination.views import AjaxListView
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.db.models import Q
from django.contrib.staticfiles.templatetags.staticfiles import static
 
def index(request):
    my_dict = {'insert_me':"hello, I am from views"}
    return render(request,'index.html',context=my_dict)
  









