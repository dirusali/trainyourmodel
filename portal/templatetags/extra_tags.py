from datetime import datetime
from scan.models import SearchTag, RatedProduct, CategoryImage
from django import template
import json
import ast
register = template.Library()

@register.assignment_tag
def get_cheapest(best5=None):
    best5=json.loads(best5)
    min=999999
    index=0
    for idx, product in enumerate(best5):
        if product['price'] < min:
            min = product['price']
            index = idx

    return index

@register.assignment_tag
def get_best5(best5=None):
    return json.loads(best5)

@register.filter(name='getlist')
def getlist(value):
    return ast.literal_eval(value)

@register.simple_tag
def multiply(value):
    return value * 6

@register.simple_tag
def convertlist(pricelist):
    for i in pricelist:
        for precios, times in dictionary.items():
            par = [times,float(precios)]
            lista.append(par)    
    return lista
    

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

@register.filter(name='icat')
def get_image_cat(value):
    try:
        result = CategoryImage.objects.get(name=value['category']).image.url
    except CategoryImage.DoesNotExist:
        try:
            result = SearchTag.objects.filter(category=value['category']).filter(
                is_valid=True).first().best5_links.first().medium_image_url
        except:
            result = False
    except Exception:
        result = False
    return result

#@register.filter(name='itag')
#def get_image_tag(value):
#    
#        result = SearchTag.objects.filter(tag=value.tag).filter(is_valid=True).last().best5_links.first().large_image_url
#        if (result == ''):
#            try:
#                result = SearchTag.objects.filter(tag=value.tag).filter(is_valid=True).last().best5_links.first().medium_image_url
#            except:
#                return '/static/images/none.jpg'
#        return result    

@register.filter(name='itag')
def get_image_tag(value):
    try:
        b5 = []
        name = value.tag
        tag = SearchTag.objects.filter(is_active=True).filter(tag=name)
        links = tag.values('best5_links')
        for i in links:
            a = i.get('best5_links', None)
            p = RatedProduct.objects.get(id=a)
            b5.append(p)
        orden = sorted(b5, key=lambda x: float(x.relevance))
        mejor = orden[0]
        result = mejor.large_image_url
        if len(result) == 0:
            result=mejor.medium_image_url
    except:
        return '/static/images/none.jpg'
    return result

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

@register.filter(name='transport')
def transport(product):
    transport = 7.5

    if product.searchtag.through.objects.first().searchtag.root in ['music', 'dvd', 'software', 'videogames']:
        transport = 5

    return transport + ( 1.3 * product.weight )

@register.filter
def modulo(num, val):
    return num % val == 0

@register.filter
def category_url(tag):
    cat = tag.category_slug
    url = "www.thebest5.com/uk/" + str(cat)
    return url

@register.filter
def to_https(url):
    url = url[4:]
    url = 'https' + url
    return url
