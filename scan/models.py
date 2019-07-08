
from django.db import models, OperationalError, transaction
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
import json
from django_mysql.models import ListTextField
from django.utils import timezone
from model_utils.models import TimeStampedModel
from lxml import html
import collections
import logging
from django.db.models import Count, CharField, Model
from django.urls import reverse
logger = logging.getLogger(__name__)
from datetime import datetime
from django.template.defaultfilters import truncatechars

class RatedProduct(TimeStampedModel):
    medium_image_url = models.CharField(max_length=500, blank=True)
    large_image_url = models.CharField(max_length=2000, blank=True, default='')
    recommend_percentage = models.FloatField(default=0)
    over_rank_percentage = models.FloatField(default=0)
    brand = models.CharField(max_length=200, blank=True, null=True)
    editorial_review = models.CharField(max_length=10000, blank=True)
    features = models.CharField(max_length=5000,blank=True)
    prime = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    old_price = models.FloatField(default=0)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    price_UK = models.FloatField(default=0, blank=True, null=True)
    price_DE = models.FloatField(default=0, blank=True, null=True)
    price_FR = models.FloatField(default=0, blank=True,null=True)
    price_IT = models.FloatField(default=0, blank=True, null=True)
    price_US = models.FloatField(default=0, blank=True, null=True)
    title = models.CharField(max_length=500,blank=True)
    sales_rank = models.CharField(max_length=200, default="100")
    rank = models.FloatField(default=0)
    ratings_rank = models.PositiveIntegerField(default=0)
    asin = models.CharField(max_length=150)
    isbn = models.CharField(max_length=150, null=True, blank=True)
    model = models.CharField(max_length=2000, null=True, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    is_valid = models.BooleanField(default=False)
    weight = models.FloatField(default=0)
    product_detail_html = models.TextField(blank=True, help_text="Caraterísticas del producto obtenidas de la tabla de IDEALO")
    active = models.BooleanField(default=True)
    product_details = models.TextField(blank=True, help_text="product details from amazon web")
    pros = models.TextField(null=True, blank=True)
    cons = models.TextField(null=True, blank=True)
    price_list = ListTextField(base_field=CharField(max_length=25,blank=True,null=True), blank=True, size=10000)
    exception = models.BooleanField(default=False)
    scanned = models.BooleanField(default=False)
    tried_scan = models.BooleanField(default=False)
    no_ean = models.BooleanField(default=False)
    price_alert = ListTextField(base_field=CharField(max_length=25,blank=True,null=True), blank=True, size=10000)
    pricetimes = ListTextField(base_field=CharField(max_length=25,blank=True,null=True), blank=True,size=10000)
    amazon_stock= models.BooleanField(default=False)
    ebay = models.BooleanField(default=False)
    ean_list = ListTextField(base_field=CharField(max_length=25,blank=True,null=True), blank=True, size=10000)
    relevance = models.FloatField(default=0, null=True)
    unavailable = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    def _parse_product_detail_html(self):
        html_doc = self.product_detail_html
        XPATH = '//*[@id="Características técnicas"]/ul/li'
        parser = html.fromstring(html_doc)
        xpath = parser.xpath(XPATH)
        group = ''
        for li in xpath:
            span_list = li.xpath('span')
            if len(span_list) == 0:
                group = li.text.strip()
            else:
                product_att = span_list[0].text.strip()
                product_value = span_list[1].text.strip()
                rtp, created = RatedProductAttribute.objects.update_or_create(product = self,
                                                                              attribute=product_att,
                                                                              defaults={'value':product_value, 'group':group})

    def save(self, *args, **kwargs):
        if self.pk:
            if self.product_detail_html:
                self._parse_product_detail_html()       
        super(RatedProduct, self).save(*args, **kwargs)
    
class RatedProductAttribute(models.Model):
    product = models.ForeignKey(RatedProduct, related_name="details")
    attribute = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    group = models.CharField(max_length=200, blank=True)
    show = models.BooleanField(default=True, help_text="Decide if the attribute will be showed at public site")

    def __str__(self):
        return '%s - %s' % (self.product, self.attribute)

class SearchTagActiveManager(models.Manager):
    """
    Manager that filter only *active* searchtags.
    """

    def get_queryset(self):
        return super(SearchTagActiveManager, self).get_queryset().filter(is_active = True)

class SearchTag(models.Model):
    tag = models.CharField(max_length = 500, blank=True, db_index=True)
    root = models.CharField(max_length = 100, blank=True)
    category = models.CharField(max_length = 200, blank=True)
    path = models.CharField(max_length = 500, blank=True)
    priority = models.PositiveSmallIntegerField(default=1)
    last_scanned = models.DateTimeField(null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)
    category_slug = AutoSlugField(populate_from='category', always_update=True)
    best5 = models.TextField(blank=True)
    best5_links = models.ManyToManyField(RatedProduct, blank=True, related_name='searchtag')
    rated_reviews = models.PositiveIntegerField(default=0)
    toy = models.TextField(max_length=20, blank=True, null=True)
    scanned_times = models.PositiveIntegerField(default=0)
    is_valid = models.BooleanField(default=True)
    is_scanned = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    is_promoted = models.BooleanField(default=False)
    female = models.BooleanField(default=False)
    alias = models.CharField(max_length=300, blank=True, db_index=True)
    browsenode = models.CharField(max_length=50, blank=True)
    include_unrated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False, db_index=True, help_text='if the searchtag will be public (active) or not')
    seo_description = models.CharField(max_length=255, blank=True)
    seo_title = models.CharField(max_length=55, blank=True)
    for_him = models.BooleanField(default=False)
    for_her = models.BooleanField(default=False)    
    objects = models.Manager()
    active_objects = SearchTagActiveManager()
    scrapper = models.BooleanField(default=False)
    excluded= ListTextField(base_field=CharField(max_length=20,blank=True),blank=True,size=10000)
    social_image = models.CharField(max_length=2000, blank=True,null=True)
    header_image = models.CharField(max_length=2000, blank=True,null=True)
    options = models.BooleanField(default=False)
    pictures = models.BooleanField(default=False)
    related_tags = ListTextField(base_field=CharField(max_length=20,blank=True),blank=True,size=10000)
    bestsellers = models.BooleanField(default=False)
    pictures_second = models.BooleanField(default=False)
    under_15 = models.BooleanField(default=False)
    scrap_browsenode = models.BooleanField(default=False)
    nofollow =  models.BooleanField(default=True)

    class Meta:
        ordering = ['slug']

    def get_absolute_url(self):
        return reverse('portal:detail', args=[str(self.slug)])
              
    def save(self, *args, **kwargs):
        # Update slug
        slug = slugify(self.tag)
        if self.slug != slug:
            self.slug = slug  
        return super(SearchTag, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.slug
