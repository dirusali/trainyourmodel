
from django.views.generic import TemplateView
#nuevo para redirecciones de url
from django.views.generic.base import RedirectView
from portal import views as portal_views

app_name = 'portal'

from .views import HomeView, FuncionaView, ContactoView, FaqView, TiendasView, RegistroTiendaView, TiendasDetail, CondicionesView, PrivacidadView, SearchTagApi, SearchTagDetail, SearchTagDetailFemale, SearchTagCategoriesList, SearchTagCategoriesDetail, \
    SearchTagView, subscribe, alerts, opinion, shopopinion, TradeDoublerVerificationView, AjaxTagProductsView, registro, successRegistroTiendaView, successView, RegalosEllosView, RegalosEllasView, contacto


urlpatterns = [
    url(r'^/$', HomeView.as_view(), name='home'),
    url('/error404/$', portal_views.error404, name='error404'),
    url('/error500/$', portal_views.error500, name='error500'),
    url('/message-sent/', successView, name='success'),
    url(r'^/gifts-for-men/$', RegalosEllosView.as_view(), name='regalos-ellos'),
    url(r'^/gifts-for-women/$', RegalosEllasView.as_view(), name='regalos-ellas'),
    url(r'^/petition-sent/$', successRegistroTiendaView, name='registro-tienda'),
        url(r'^/categories/$', SearchTagCategoriesList.as_view(), name='categories'),
        url(r'^/category/(?P<slug>[-\w]+)/$', SearchTagCategoriesDetail.as_view(), name='categories-detail'),
        url(r'^/search/$', SearchTagView.as_view(), name='search'),
        url(r'^/query/$', SearchTagApi.as_view(), name='query'),
        url(r'^/terms-and-conditions/$', CondicionesView.as_view(), name='terms'),
        url(r'^/privacy/$', PrivacidadView.as_view(), name='priv'),
        url(r'^/faq/$', FaqView.as_view(), name='faq'),
        url(r'^/how-it-works/$', FuncionaView.as_view(), name='funciona'),
        url(r'^/best-(?P<slug>[-\w]+|)/$', SearchTagDetail.as_view(), name='detail'),
        url(r'^/best(?P<slug>[-\w]+|)/$', SearchTagDetailFemale.as_view(), name='detail-female'),
        url(r'^/subscribe/', subscribe, name="subscribe"),
        url(r'^/contact/', contacto, name="contacto"),
        url(r'^/register-shop/$', RegistroTiendaView.as_view(), name='registrar-tienda'),
        url(r'^/contact/$', ContactoView.as_view(), name='contacto'),
        url(r'^/about/$', RedirectView.as_view(url='/como-funciona/', permanent=True)),
]

