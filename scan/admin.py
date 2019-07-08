from django.contrib import admin
#from scan.forms import  ProductExceptionForm, ScrapperToleranceForm
from .models import DataFile

class DataFileAdmin(admin.ModelAdmin):
    search_fields=['title']
    list_display=['title']
    list_filter = ('title',)
    
                    
admin.site.register(DataField,DataFieldAdmin)
