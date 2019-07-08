from django.contrib import admin
from scan.forms import  ProductExceptionForm, ScrapperToleranceForm
from .models import SearchTag, RatedProduct, AffiliationNetwork, CategoryImage, ProductPurchaseOption, ProductException, \
    ScrapperTolerance, RatedProductAttribute, Article, Opinion, Shop, OpinionShop, PurchaseOptionException

class SearchTagAdmin(admin.ModelAdmin):
    search_fields=['tag', 'slug', 'category', 'root', 'path']
    list_display = ('tag', 'browsenode', 'last_scanned','category', 'nofollow', 'for_him', 'for_her', 'rated_reviews', 'is_active', 'scrapper', 'options')
    list_filter=('category','root', 'include_unrated')
    readonly_fields = ('slug','category_slug',)
    raw_id_fields = ("best5_links",)
    actions = ['is_nofollow', 'is_not_nofollow','scrap_browsenode', 'poner_paraellos', 'quitar_paraellos', 'poner_paraellas', 'quitar_paraellas', 'not_bestseller','is_bestseller', 'change_to_female', 'change_to_male', 'add_scrapper', 'remove_scrapper', 'add_options', 'remove_options', 'yes_pictures', 'no_pictures']
   
    def scrap_browsenode(self, request, queryset):
        queryset.update(scrap_browsenode=True)
    
    def poner_paraellos(self, request, queryset):
        queryset.update(for_him=True)
    
    def quitar_paraellos(self, request, queryset):
        queryset.update(for_him=False)   
     
    def poner_paraellas(self, request, queryset):
        queryset.update(for_her=True)
    
    def quitar_paraellas(self, request, queryset):
        queryset.update(for_her=False) 
        
    def yes_pictures(self, request, queryset):
        queryset.update(pictures_second=True)
        
    def no_pictures(self, request, queryset):
        queryset.update(pictures_second=False)
     
    def add_options(self, request, queryset):
        queryset.update(options=True)
        
    def remove_options(self, request, queryset):
        queryset.update(options=False)
    
    def add_scrapper(self, request, queryset):
        queryset.update(scrapper=True)
        
    def remove_scrapper(self, request, queryset):
        queryset.update(scrapper=False)    
    
    def change_to_female(self, request, queryset):
        queryset.update(female=True)
           
    def change_to_male(self, request, queryset):
        queryset.update(female=False)
        
    def is_bestseller(self, request, queryset):
        queryset.update(bestsellers=True) 
        
    def not_bestseller(self, request, queryset):
        queryset.update(bestsellers=False) 
     
    def is_nofollow(self, request, queryset):
        queryset.update(nofollow=True) 
        
    def is_not_nofollow(self, request, queryset):
        queryset.update(nofollow=False)  
           
class RatedProductAttributeInline(admin.TabularInline):
    model = RatedProductAttribute
    fields = ('attribute', 'value', 'group')

class ProductPurchaseOptionInline(admin.TabularInline):
    model = ProductPurchaseOption

class RatedProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_list', 'price', 'modified', 'brand', 'is_valid', 'scanned','ebay', 'ean', 'no_ean', )
    search_fields=['title', 'ean', 'asin']
    list_filter=('brand','searchtag',)
    inlines = [RatedProductAttributeInline, ProductPurchaseOptionInline]
    actions = ['yes_ean']
    
    def yes_ean(self, request, queryset):
        queryset.update(no_ean=False)
            
               
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('product_short', 'name', 'email', 'valid', 'rating', 'opinion', 'date')
    search_fields = ['title']
    actions = ['valid', 'not_valid']
   
    def valid(self, request, queryset):
        queryset.update(valid=True) 
        
    def not_valid(self, request, queryset):
        queryset.update(valid=False)  
        
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'slug', 'logo', 'active', 'url', 'url_affiliate')
    search_fields = ['shop']
    
class OpinionShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'rated_shop', 'comentario', 'name', 'email', 'rating', 'valid')
    search_fields = ['name']
    
class AffiliationNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'enabled')
    search_fields = ['name']
    list_filter = ('enabled',)

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['slug']
    list_display = ('slug', 'is_ready', 'date', 'title')
    
class ProductPurchaseOptionAdmin(admin.ModelAdmin):
    list_display = ('short_product','shop_name', 'price', 'shop_logo') 
    search_fields = ['purchase__name']
    list_filter = ('product','price','shipping_cost','shop_name',)
    raw_id_fields = ['product', 'source_net']

class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'icon', 'image_header', 'category_description', 'category_title', 'category_anchor',)
    link_display_links = list_display
    search_fields = ['name']

class ProductExceptionAdmin(admin.ModelAdmin):
    form = ProductExceptionForm
    list_display = ('tag', 'product', )
    search_fields = ['product__title', 'product__brand']

class ScrapperToleranceAdmin(admin.ModelAdmin):
    form = ScrapperToleranceForm
    list_display = ('tag', 'shop_name', 'words_match', 'similarity', 'price_delta', 'chisqr_similarity',)
    search_fields = ['tag__tag', 'tag__slug', 'tag__category', 'tag__root', 'tag__path', 'shop_name']
    list_filter = ('shop_name', 'tag', )


class PurchaseOptionExceptionAdmin(admin.ModelAdmin):
    list_display = ('name','url')
    search_fields = ['name']
    list_filter = ('name',)
    
                    
admin.site.register(RatedProduct,RatedProductAdmin)
admin.site.register(SearchTag, SearchTagAdmin)
admin.site.register(AffiliationNetwork, AffiliationNetworkAdmin)
admin.site.register(ProductPurchaseOption, ProductPurchaseOptionAdmin)
admin.site.register(CategoryImage, CategoryImageAdmin)
admin.site.register(ProductException, ProductExceptionAdmin)
admin.site.register(ScrapperTolerance, ScrapperToleranceAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(OpinionShop, OpinionShopAdmin)
admin.site.register(Shop,ShopAdmin)
admin.site.register(PurchaseOptionException,PurchaseOptionExceptionAdmin)
