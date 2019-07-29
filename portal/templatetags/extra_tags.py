from datetime import datetime
from django import template
import pandas as pd
import numpy as np
import json
import ast
register = template.Library()


@register.filter(name='getlist')
def getlist(value):
    return ast.literal_eval(value)

@register.simple_tag
def multiply(value):
    return value * 6
    
@register.simple_tag
def frame(values):
    df = pd.DataFrame(values)
    return df

@register.simple_tag
def current_month():
    month = datetime.now().month
    if str(month) == '1':
        mes = 'Ene'
    if str(month) == '2':
        mes = 'Feb'
    if str(month) == '3':
        mes = 'Mar'
    if str(month) == '4':
        mes = 'Abr'
    if str(month) == '5':
        mes = 'May'
    if str(month) == '6':
        mes = 'Jun'
    if str(month) == '7':
        mes = 'Jul'
    if str(month) == '8':
        mes = 'Ago'
    if str(month) == '9':
        mes = 'Sep'
    if str(month) == '10':
        mes = 'Oct'
    if str(month) == '11':
        mes = 'Nov'
    if str(month) == '12':
        mes = 'Dic'    
    return mes

@register.simple_tag
def divide(value):
    value = (value * 3) / 1000
    value = str(value)
    partes = value.split('.')
    ent = partes[0]
    ent = ent + ','
    dec = partes[1]
    if len(dec) == 2:
        dec = dec + '0'
    if len(dec) == 1:
        dec = dec + '00'
    if len(dec) == 0:
        dec = dec + '000'
    value = ent + dec
    return value 




@register.filter(name='format_tooltip')
def format_tooltip(value):
    return " ".join(value.split('.'))

@register.filter(name='remove_ellipsis')
def remove_ellipsis(value):
    return " ".join(value.split('...'))

@register.filter(name='uktoeur')
def uktoeur(value):
    return value / 0.86


@register.simple_tag
def priceformat(value):
    value = str(value).replace(",",".")
    return value 



@register.filter
def modulo(num, val):
    return num % val == 0


@register.filter
def to_https(url):
    url = url[4:]
    url = 'https' + url
    return url
