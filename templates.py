{% load static %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es-ES">
<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1.0, user-scalable=no">
<link href="https://fonts.googleapis.com/css?family=Lato:300,400,700,900|Oswald:300,400,500,600,700" rel="stylesheet">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.13/css/all.css" integrity="sha384-DNOHZ68U8hZfKXOrtjWvjxusGo9WQnrNx2sqG0tfsghAvtVlRW3tvkXWZh58N9jp" crossorigin="anonymous">
<link href="{% static 'semantic/dist/semantic.min.css' %}" rel="stylesheet">
<link rel="stylesheet" href="{% static 'best5/css/style.css' %}" type="text/css" media="screen" />
<link rel="shortcut icon" href="{% static 'images/favicon/favicon.png' %}" type="image/x-icon">
<link rel="icon" href="{% static 'images/favicon/favicon.png' %}" type="image/x-icon">
<link rel="apple-touch-icon" sizes="57x57" href="{% static 'images/favicon/apple-icon-57x57.png' %}">
<link rel="apple-touch-icon" sizes="60x60" href="{% static 'images/favicon/apple-icon-60x60.png' %}">
<link rel="apple-touch-icon" sizes="72x72" href="{% static 'images/favicon/apple-icon-72x72.png' %}">
<link rel="apple-touch-icon" sizes="76x76" href="{% static 'images/favicon/apple-icon-76x76.png' %}">
<link rel="apple-touch-icon" sizes="114x114" href="{% static 'images/favicon/apple-icon-114x114.png' %}">
<link rel="apple-touch-icon" sizes="120x120" href="{% static 'images/favicon/apple-icon-120x120.png' %}">
<link rel="apple-touch-icon" sizes="144x144" href="{% static 'images/favicon/apple-icon-144x144.png' %}">
<link rel="apple-touch-icon" sizes="152x152" href="{% static 'images/favicon/apple-icon-152x152.png' %}">
<link rel="apple-touch-icon" sizes="180x180" href="{% static 'images/favicon/apple-icon-180x180.png' %}">
<link rel="icon" type="image/png" sizes="192x192"  href="{% static 'images/favicon/android-icon-192x192.png' %}">
<link rel="icon" type="image/png" sizes="32x32" href="{% static 'images/favicon/favicon-32x32.png' %}">
<link rel="icon" type="image/png" sizes="96x96" href="{% static 'images/favicon/favicon-96x96.png' %}">
<link rel="icon" type="image/png" sizes="16x16" href="{% static 'images/favicon/favicon-16x16.png' %}">
<link rel="manifest" href="{% static 'images/favicon/manifest.json' %}">
  
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="msapplication-TileImage" content="{% static 'images/favicon/ms-icon-144x144.png' %}">
<title>{% block title %}The Best 5{% endblock %}</title>
{% block meta %}<link rel="publisher" href="https://plus.google.com/u/0/115567898557132319434" />{% endblock %}
<script>
  dataLayer = [];
</script>
{% comment %}<!-- Google Tag Manager -->{% endcomment %}
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-5Z2PWFQ');</script>
{% comment %}<!-- End Google Tag Manager -->{% endcomment %}

{% comment %}<!-- For Admitad affiliation network -->{% endcomment %}
<meta name="verify-admitad" content="376e0c1f16" />
{% comment %}<!-- For Zanox affiliation network -->{% endcomment %}
<meta name="verification" content="fc86394353de3fcac7ff2c76b3800123" />
<meta name="google-site-verification" content="o3kkJc1Tv0ks3i50VwYl9MxqkIVkjv3DuHGqDI1Uj3w" />
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-102150447-2');
  </script>
  <meta name="theme-color" content="#ffffff">
  {% comment %}<!-- Facebook Pixel Code -->{% endcomment %}
  <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window,document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
     fbq('init', '1834454873475427');
    fbq('track', 'PageView');
  </script>
  <noscript>
    <img height="1" width="1" src="https://www.facebook.com/tr?id=1834454873475427&ev=PageView&noscript=1"/>
  </noscript>
{% comment %}<!-- End Facebook Pixel Code -->{% endcomment %}
<script src="{% static 'best5/js/jquery-3.3.1.min.js' %}"></script>
{% if is_home %}
  <script src="{% static 'best5/js/owl.carousel.min.js' %}"></script>
{% endif %}
</head>
<body>  
{% block content %}{% endblock %} 
{% comment %}<!-- footer -->{% endcomment %}
<footer id="footer">
  <div class="newsletter">
    <div class="container medium">
      <div class="txt">
        <p>Los productos mejor recomendados, en UN CLICK, y no pierdas más tiempo. ¿Te apuntas?</p>
        <div class="guia">
          <span class="ico"></span>
          <p>Descárgate GRATIS nuestro eBook de 5 TRUCOS PARA COMPRAR ONLINE MÁS BARATO</p>
        </div>
      </div>
      <a id="suscripcion-footer" href="#" data-fancybox data-src="#newsletter" class="btn" rel="nofollow">Descargar eBook</a>
      </div>
    </div>
  </div>
  <div class="main">
    <div class="container">
      <div class="main-1">
        <img src="{% static 'images/logo-white.png' %}" alt="Logo Thebest5" width="200" class="logo" />
        <ul>
          <li><a href="https://{{request.get_host}}/registrar-tienda/">Registrar tienda</a></li>
          <li><a href="https://{{request.get_host}}/como-funciona/" title="Ver cómo funciona el recomendador The Best 5">¿Cómo funciona?</a></li>
          <li><a href="https://{{request.get_host}}/tiendas-thebest5/" title="Ver tiendas de The Best 5">Ver todas las tiendas</a></li>
          <li><a href="https://{{request.get_host}}/preguntas-frecuentes/" title="Preguntas frecuentes acerca de The Best 5">FAQ</a></li>
          <li><a href="https://www.thebest5.es/blog/" target="_blank" title="Ir al Blog The Best 5">Blog</a></li>
          <li><a href="https://{{request.get_host}}/politica-de-privacidad/" rel="nofollow">Política de privacidad</a></li>
          <li><a href="https://{{request.get_host}}/terminos-y-condiciones/" rel="nofollow">Términos y condiciones</a></li>
          <li><a href="https://{{request.get_host}}/contacto/" rel="nofollow">Contacto</a></li>
        </ul>
      </div>
      <div class="main-2">
        <ul>
          {% if normal_footer_cat %}
            {% for category in categories %}
                  <li><a href="{% url 'portal:categories-detail' slug=category.category|slugify %}" title="Ver {% if object.female %}las{% else %}los{% endif %} mejores Artículos de {{ category.category }}">{{ category.category|title }}</a></li>
                  {% if forloop.counter == 10 %}
                  </ul>
                  <ul>
                  {% endif %}
              {% endfor %}
          {% else %}
              {% if is_search %}
                  {% for tag in tag_list|slice:":14" %}
                        <li><a href="{% if tag.female %}{% url 'portal:detail-female' slug=tag.slug %}{% else %}{% url 'portal:detail' slug=tag.slug %}{% endif %}" title="Ver {% if tag.female %}las{% else %}los{% endif %} mejores {{tag.tag}}">{% if tag.female %}Las{% else %}Los{% endif %} mejores {{tag.tag|lower}} de {{current_anno}}</a></li>
                        {% if forloop.counter == 7 %}
                        </ul>
                        <ul>
                        {% endif %}
                        {% if forloop.counter == 14 %}
                        </ul>
                        {% endif %}
                  {% endfor %}
              {% else %}
                {% for related_link in related_links|slice:":14" %}
                   <li><a href="{% if related_link.female %}{% url 'portal:detail-female' slug=related_link.slug %}{% else %}{% url 'portal:detail' slug=related_link.slug %}{% endif %}" class="prev" title="Quiero encontrar {% if related_link.female %}las{% else %}los{% endif %} 5 mejores {{related_link.tag}} de {{current_anno}}">{% if related_link.female %}Las{% else %}Los{% endif %} mejores {{related_link.tag|lower}} de {{current_anno}}</a></li>
                    {% if forloop.counter == 7 %}
                      </ul>
                      <ul>
                    {% endif %}
                    {% if forloop.counter == 14 %}
                      </ul>
                    {% endif %}
                {% endfor %}
              {% endif %}
          {% endif %}
        </ul>
      </div>
    </div>
    <div style="text-align:center;font-size:12px;padding:25px 40px 5px 35px;color: #d1ecde;margin-bottom: -30px;">*Los precios se indican en Euros e incluyen IVA, pero no los gastos de envío. Puede haber cambios en el precio, la clasificación, las disponibilidad y los gastos. El precio final será, en todo caso, aquel mostrado en las webs a las que redirigimos.</div>
  </div>
  <div class="copy">
    <div class="container">
      <p>@The Best 5 {{current_anno}}</p>
      <ul class="social">
        <li><a href="https://www.instagram.com/thebest5spain/" class="instagram" target="_blank"><span class="fab fa-instagram"></span></a></li>
        <li><a href="https://www.facebook.com/thebest5spain/" target="_blank" class="facebook"><span class="fab fa-facebook-f"></span></a></li>
        <li><a href="https://plus.google.com/u/0/115567898557132319434" target="_blank"  class="google"><span class="fab fa-google-plus-g"></span></a></li>
      </ul>
    </div>
  </div>
  <a href="#" class="scroll-top"></a>
</footer>
{% comment %}<!-- tab newsletter -->{% endcomment %}
<div class="tab-newsletter">
  <a href="#" data-fancybox data-src="#newsletter" rel="nofollow"><span class="ico"></span><span class="txt">TRUCOS PARA COMPRAR MÁS BARATO</a>
</div>
<div class="lightbox newsletter" id="newsletter" style="max-width:50%;">
    <div class="mobile only row">
      <div class="ui mailchimp mobile">
            <div class="content ui three column centered grid" id="modal_img">
                <div class="one column centered row">
                    <div class="column" id="mensaje">
                        <h2 class="ui center aligned header" style="color: #FFF">
                            Descárgate GRATIS nuestro eBook de 5 TRUCOS PARA COMPRAR ONLINE MÁS BARATO
                        </h2>
                        <div id="boton-guia-compra" class="centered row" style="display:none;">
                          <div class="six wide column">
                              <a href="{% static 'pdf/5-trucos-para-comprar-online-más-barato-The-Best-5.pdf' %}" target="_blank" title="Descargar eBook"><button type="submit" class="fluid ui primary button">Descargar eBook</button></a>
                          </div>
                    </div>
                </div>
                <div  id="formulario" class="one column centered row">
                    <div class="column">
                        <div class="subscribe_form">
                            <form id="subscribe-mobile" class="ui form subscribe" method='POST' action="{% url 'portal:subscribe' %}">
                            {% csrf_token %}
                                <div id="search-box" class="ui transparent input field" style="border:1px solid #ccc; border-radius:65px; background-color:#ffffff; padding-left:10px;">
                                    <input id="email_id" name="email" type="email" required placeholder="Escribe aquí tu correo electrónico para descargarlo"
                                           style="min-width: 420px;font-weight:300; font-family: 'Poppins', sans-serif;font-size:1.7em;">
                                </div>
                                <div class="ui two column centered grid">
                                    <div class="centered row">
                                    <input type="checkbox" id="terminos" required />
         <label for="terminos" style="color: white;margin-top:-6px;margin-left: 5px;">Acepto <a href="https://{{request.get_host}}/terminos-y-condiciones/" rel="nofollow" target="_blank" style="color:antiquewhite;text-decoration:underline;">términos y condiciones</a> y la <a href="https://{{request.get_host}}/politica-de-privacidad/" rel="nofollow" target="_blank" style="color:antiquewhite;text-decoration:underline;">política de privacidad</a></label>
                                    </div>
                                    <div class="centered row">
                                      <div class="six wide column">
                                        <button type="submit" class="fluid ui primary button">
                                          Descargar eBook
                                        </button>
                                      </div>
                                    </div>
                                </div>
                             </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% comment %}<!-- ./tab newsletter -->{% endcomment %}
<link rel="stylesheet" type="text/css" href="//cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.css" />
<script src="//cdnjs.cloudflare.com/ajax/libs/cookieconsent2/3.1.0/cookieconsent.min.js"></script>
<script>
window.addEventListener("load", function(){
window.cookieconsent.initialise({
  "palette": {
    "popup": {
      "background": "#3d3f4a",
      "text": "#ffffff"
    },
    "button": {
      "background": "#88c59f",
      "text": "#ffffff"
    }
  },
  "theme": "classic",
  "content": {
    "message": "Utilizamos cookies para medir el tráfico del sitio web y mejorar la experiencia de usuario. Pulsa el botón para seguir navegando con normalidad.",
    "dismiss": "Seguir navegando",
    "link": "Leer más",
    "href": "https://www.thebest5.es/politica-de-privacidad/"
  }
})});
</script>
<script src="{% static 'semantic/dist/semantic.min.js' %}"></script>
<script src="{% static 'best5/js/animatescroll.min.js' %}"></script>
{% comment %}<script src="{% static 'best5/js/jquery.fancybox.min.js' %}"></script>{% endcomment %}
<script src="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"></script>
<script src="{% static 'best5/js/icheck.js' %}"></script>
{% if valoracionesjs or valoracionesTiendajs %}{% comment %}<!-- ./star rating plugin -->{% endcomment %}
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.3.2/jquery.rateyo.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/rateYo/2.3.2/jquery.rateyo.min.js"></script>
{% endif %}{% comment %}<!-- ./star rating plugin -->{% endcomment %}
{% if lazyjs %}
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.lazy/1.7.4/jquery.lazy.min.js"></script>
{% endif %}
<script src="{% static 'best5/js/scripts.js' %}"></script>
<script src="{% static 'django_evercookie/swfobject-2.2.min.js' %}"></script>
<script src="{% static 'best5/js/js.cookie.js' %}"></script>
<script src="/ecookie"></script>
{% load evercookie_js_api %}
{% if lazyjs %}
<script>
    $(function() {
        $('.lazy').lazy();
    });
    var $windowheight = $(window).outerHeight ();
    $('#search-container .results').css('max-height', $windowheight - 150);
    
    $( window ).resize(function() {
    $windowheight = $(window).outerHeight ();
    $('#search-container .results').css('max-height', $windowheight - 150);
  });
  
  $( window ).on( "orientationchange", function() {
    $windowheight = $(window).outerHeight ();
      $('#search-container .results').css('max-height', $windowheight - 150);
  });
</script>
{% endif %}
{% if is_home %}
<script>
    $('.slider-home').owlCarousel({
      autoplay: true,
      items: 1,
      loop: true,
      autoplayTimeout: 3000,
      smartSpeed: 350,
  });
</script>
{% endif %}
{% if valoracionesjs or valoracionesTiendajs %}
<script>
  $(".star-rating").rateYo({
    starWidth: "20px",
      normalFill: "#c3e0ce",
      ratedFill: "#87c59e",
      spacing: "3px",
      halfStar: true
    });
</script>
{% endif %}
    <script>
        $(document).ready(function(){
          {% comment %}/*device detection*/{% endcomment %}
          var isMobile = false; {% comment %}/*initiate as false*/{% endcomment %}
    
          if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
              || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
              isMobile = true;
          }
          if(isMobile) {
              window.onclick = function(event) {
                  if (event.target.className != 'toggle-menu' && event.target.className != 'bar' && event.target.id != 'menucategorias') {
                     $('#menu-mobile').css('display', 'none');
                     event.stopPropagation();
                  }
              }
          }
          {% if is_home %}
            if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
               $("#menucategorias").attr("href", "#");
            }
          {% else %}
              if(!isMobile) {
                 $("#menucategorias").attr("href", "https://www.thebest5.es/categorias/");
              }
            {% endif %}
            // Search
              $('#search-input').keypress(function(e) {
                if(e.which == 13) {
                  var url = '/buscar/?q=' + $('#search-input').val();
                  window.location = url;
                }
              })
              $('#doSearch').click(function(e) {
                  var url = '/buscar/?q=' + $('#search-input').val();
                  window.location = url;
                })
              $('.close-icon').click(function(e) {
                $('#search-input').val('');
                $('#search-input').attr("placeholder", "Busco los 5 mejores...");
              })
            // Search autocomplete
           $('.ui.search')
      .search({
        minCharacters : 3,
        maxResults: 12,
        apiSettings   : {
          onResponse: function(best5Response) {
            var
              response = {
                results : []
              }
            ;
            // translate GitHub API response to work with search
            $.each(best5Response, function(index, item) {
              var maxResults = 16;
              if(index >= maxResults) {
                return false;
              }
              if(item.female){
                mejores = '/las-mejores-';
              }else{
                mejores = '/los-mejores-';
              }
              // add result to category
              response.results.push({
                title       : item.tag,
                description : item.category,
                url         : mejores + item.slug + '/'
              });
            });
            return response;
          },
          url: '/query/?q={query}'
        }
    });
        {% if valoracionesjs %} 
        var send_opinion = function(form){
                var name = $("#name"+form).val();
                var title = $("#title"+form).val();
                var email_opinion = $("#email_opinion"+form).val();
                var opinion = $("#opinion"+form).val();
                var rating = $("#star-rating"+form).rateYo("rating");
                var FormId = $("#FormId"+form).val();
                var ProdId = $("#ProdId"+form).val();
            if(email_opinion){
                var csrfmiddlewaretoken = csrftoken;
                var opinion_data = {"title": title,"name": name,"email_opinion": email_opinion,
                    "opinion": opinion,"rating": rating,"FormId": FormId,"ProdId": ProdId,"csrfmiddlewaretoken" : csrfmiddlewaretoken};
                $.ajax({
                    type: 'POST',
                    url:  '/opinion/',
                    data: opinion_data,
                    success: function(response){
                        if(response.status == "404"){
                            $('.error-notification').slideDown('fast');
                            window.setTimeout(closeOpinionError,4000);
                            function closeOpinionError() {
                              $('.error-notification').slideUp('fast');
                            }
                        }
                        else{
                            $('.notification').slideDown('fast');
                            window.setTimeout(closeOpinion,4000);
                            function closeOpinion() {
                              $('.notification').slideUp('fast');
                              $("[name='title"+form+"']").val('');
                              $("[name='name"+form+"']").val('');
                              $("[name='email_opinion"+form+"']").val('');
                              $("#star-rating").rateYo("option", "rating", "0");
                              $("[name='opinion"+form+"']").val('');
                              $('input[name=terminos]').attr('checked', false);
                              $.fancybox.close();
                            }
                        }
                    },
                    error: function(response) {
                        alert("No se ha podido enviar tu opinión, por favor inténtalo más tarde. Muchas gracias");
                    }
                });
                return false;
            }
        };
        var send_alert = function(form){
                var price_alert = $("#importe_alert"+form).val();
                var email_alert = $("#email_alert"+form).val();
                var FormId = $("#FormId"+form).val();
                var ProdId = $("#ProdId"+form).val();
            if(email_alert){
                var csrfmiddlewaretoken = csrftoken;
                var alert_data = {"price_alert": price_alert,"email_alert": email_alert,
                    "FormId": FormId,"ProdId": ProdId,"csrfmiddlewaretoken" : csrfmiddlewaretoken};
                $.ajax({
                    type: 'POST',
                    url:  '/alerts/',
                    data: alert_data,
                    success: function(response){
                        if(response.status == "404"){
                            $('.error-notification').slideDown('fast');
                            window.setTimeout(closeOpinionError,4000);
                            function closeOpinionError() {
                              $('.error-notification').slideUp('fast');
                            }
                        }
                        else{
                            $('.notification').slideDown('fast');
                            window.setTimeout(closeOpinion,4000);
                            function closeOpinion() {
                              $('.notification').slideUp('fast');
                              $("[name='importe_alert"+form+"']").val('');
                              $("[name='email_alert"+form+"']").val('');
                              $('input[name=terminosalerta]').attr('checked', false);
                              $.fancybox.close();
                            }
                        }
                    },
                    error: function(response) {
                        alert("Lo sentimos, no se ha podido enviar tu petición de aviso, por favor inténtalo más tarde. Muchas gracias.");
                    }
                });
                return false;
            }
        };
        var send_alert_grafica = function(form){
                var price_alert = $("#importe_alert_grafica"+form).val();
                var email_alert = $("#email_alert_grafica"+form).val();
                var FormId = $("#FormId"+form).val();
                var ProdId = $("#ProdId"+form).val();
            if(email_alert){
                var csrfmiddlewaretoken = csrftoken;
                var alert_data = {"price_alert": price_alert,"email_alert": email_alert,
                    "FormId": FormId,"ProdId": ProdId,"csrfmiddlewaretoken" : csrfmiddlewaretoken};
                $.ajax({
                    type: 'POST',
                    url:  '/alerts/',
                    data: alert_data,
                    success: function(response){
                        if(response.status == "404"){
                            $('.error-notification').slideDown('fast');
                            window.setTimeout(closeOpinionError,4000);
                            function closeOpinionError() {
                              $('.error-notification').slideUp('fast');
                            }
                        }
                        else{
                            $('.notification').slideDown('fast');
                            window.setTimeout(closeOpinion,4000);
                            function closeOpinion() {
                              $('.notification').slideUp('fast');
                              $("[name='importe_alert_grafica"+form+"']").val('');
                              $("[name='email_alert_grafica"+form+"']").val('');
                              $('input[name=terminosalertagrafica]').attr('checked', false);
                              $.fancybox.close();
                            }
                        }
                    },
                    error: function(response) {
                        alert("Lo sentimos, no se ha podido enviar tu petición de aviso, por favor inténtalo más tarde. Muchas gracias.");
                    }
                });
                return false;
            }
        };
        {% endif %}
        {% if valoracionesTiendajs %} 
        var send_opinion_tienda = function(){
                var shop_name = $("#shop_name").val();
                var shop_title = $("#shop_title").val();
                var shop_email_opinion = $("#shop_email_opinion").val();
                var shop_opinion = $("#shop_opinion").val();
                var shop_rating = $("#shop_star-rating").rateYo("rating");
                var ShopId = $("#ShopId").val();
            if(shop_email_opinion){
                var csrfmiddlewaretoken = csrftoken;
                var shop_opinion_data = {"shop_title": shop_title,"shop_name": shop_name,"shop_email_opinion": shop_email_opinion,
                    "shop_opinion": shop_opinion,"shop_rating": shop_rating,"ShopId": ShopId,"csrfmiddlewaretoken" : csrfmiddlewaretoken};
                $.ajax({
                    type: 'POST',
                    url:  '/shop-opinion/',
                    data: shop_opinion_data,
                    success: function(response){
                        if(response.status == "404"){
                            $('.error-notification').slideDown('fast');
                            window.setTimeout(closeOpinionError,4000);
                            function closeOpinionError() {
                              $('.error-notification').slideUp('fast');
                            }
                        }
                        else{
                            $('.notification').slideDown('fast');
                            window.setTimeout(closeOpinion,4000);
                            function closeOpinion() {
                              $('.notification').slideUp('fast');
                              $("[name='shop_title']").val('');
                              $("[name='shop_name']").val('');
                              $("[name='shop_email_opinion']").val('');
                              $("#shop_star-rating").rateYo("option", "rating", "0");
                              $("[name='shop_opinion']").val('');
                              $('input[name=shop_terminos]').attr('checked', false);
                              $.fancybox.close();
                            }
                        }
                    },
                    error: function(response) {
                        alert("No se ha podido enviar tu opinión, por favor inténtalo más tarde. Muchas gracias");
                    }
                });
                return false;
            }
        };
        {% endif %}
        var send_subscription = function(is_mobile){
                var email = $("#email_id").val();
            if(email){
                var csrfmiddlewaretoken = csrftoken;
                var email_data = {"email": email,
                    "csrfmiddlewaretoken" : csrfmiddlewaretoken};
                $.ajax({
                    type: 'POST',
                    url:  '/subscribe/',
                    data: email_data,
                    success: function(response){
                        $( "[name='email']" ).val('');
                        if(response.status == "404"){
                            setCookieSubscribed();
                            $('#mensaje h2').empty();
                            $("#mensaje h2").text('Esa cuenta de correo ya está suscrita a nuestro boletín.');
                            $('#terminos').prop('checked', false);
                            $('.ui.modal.mailchimp.mobile').modal('hide');
                        }
                        else{
                            subs = setCookieSubscribed();
                            $('#formulario').hide();
                            $('#mensaje h2').empty();
                            $("#mensaje h2").html('Ya puedes descargar nuestro eBook pulsando en el botón.');
                            $('#boton-guia-compra').show();
                            $('.ui.modal.mailchimp.mobile').modal('hide');
                        }
                    },
                    error: function(response) {
                        alert("Error en suscripción. Por favor inténtalo de nuevo. Muchas gracias");
                        $("[name='email']").val('');
                    }
                });
                return false;
            }
        };
        $(".tab-newsletter, #suscripcion-footer").click(function(e) {
          $('#boton-guia-compra').hide();
          $('#formulario').show();
          $('#terminos').prop('checked', false);
          $('#mensaje h2').empty();
          $("#mensaje h2").html('Descárgate GRATIS nuestro eBook de 5 TRUCOS PARA COMPRAR ONLINE MÁS BARATO');
        });
        $('#subscribe-mobile').form({
            fields: {
              email:'email'
            },
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_subscription(true);
            }
        });
      {% if valoracionesjs %}
        $('#opinion_form1').form({
            fields: {
              name: 'name1',
              email_opinion: 'email_opinion1',
              opinion: 'opinion1',
            },
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_opinion('1');
            }
        });
        $('#alerts_form1').form({
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_alert('1');
            }
        });
        $('#alerts_form_grafica1').form({
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_alert_grafica('1');
            }
        });
         $('#opinion_form2').form({
            fields: {
              name: 'name2',
              email_opinion: 'email_opinion2',
              opinion: 'opinion2',
            },
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_opinion('2');
            }
        });
         $('#alerts_form2').form({
          onSuccess: function(event, fields) {
              event.preventDefault();
              send_alert('2');
          }
        });
        $('#alerts_form_grafica2').form({
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_alert_grafica('2');
            }
        });
         $('#opinion_form3').form({
            fields: {
              name: 'name3',
              email_opinion: 'email_opinion3',
              opinion: 'opinion3',
            },
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_opinion('3');
            }
        });
        $('#alerts_form3').form({
          onSuccess: function(event, fields) {
              event.preventDefault();
              send_alert('3');
          }
        });
        $('#alerts_form_grafica3').form({
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_alert_grafica('3');
            }
        });
         $('#opinion_form4').form({
            fields: {
              name: 'name4',
              email_opinion: 'email_opinion4',
              opinion: 'opinion4',
            },
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_opinion('4');
            }
        });
        $('#alerts_form4').form({
          onSuccess: function(event, fields) {
              event.preventDefault();
              send_alert('4');
          }
        });
        $('#alerts_form_grafica4').form({
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_alert_grafica('4');
            }
        });
         $('#opinion_form5').form({
            fields: {
              name: 'name5',
              email_opinion: 'email_opinion5',
              opinion: 'opinion5',
            },
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_opinion('5');
            }
        });
         $('#alerts_form5').form({
          onSuccess: function(event, fields) {
              event.preventDefault();
              send_alert('5');
          }
        });
         $('#alerts_form_grafica5').form({
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_alert_grafica('5');
            }
        });
        {% endif %}
         {% if valoracionesTiendajs %}
         $('#shop_opinion_form').form({
            fields: {
              name: 'shop_name',
              email_opinion: 'shop_email_opinion',
              opinion: 'shop_opinion',
            },
            onSuccess: function(event, fields) {
                event.preventDefault();
                send_opinion_tienda();
            }
        });
         {% endif %}
        $("#btn-already-subscribed-mobile").click(function(e){{% comment %}/*Button to allow users to stop seeing the popup in new devices*/{% endcomment %}
            $('.ui.modal.mailchimp.mobile').modal('hide');
            setCookieSubscribed();{% comment %}/*Stop showing the popup*/{% endcomment %}
        });
    });
    function setCookieSubscribed(){
        console.log("Refreshing cookies..");{% comment %}/*Set two cookies, une jquery cookie and another using evercookie*/{% endcomment %}
        console.log("Setting cookie jquery, subscribed -> YES");{% comment %}/*create jquery cookie. Set it to expire in 365 days*/{% endcomment %}
        Cookies.set('subscriptionjq', 'YES', { expires: 365 });
        var ec = new evercookie();{% comment %}/*Use evercookie to avoid problems when cookies are deleted*/{% endcomment %}
        console.log("Setting cookie evercookie, subscribed -> YES");{% comment %}/*set a cookie "id" to "12345"*/{% endcomment %}
        ec.set("subscription", "YES");
    }
    function setCookieUnsubscribed(){
        console.log("Refreshing cookies..");{% comment %}/*Set two cookies, une jquery cookie and another using evercookie*/{% endcomment %}
        console.log("Setting cookie jquery, subscribed -> NO");{% comment %}/*create jquery cookie. Set it to expire in 365 days*/{% endcomment %}
        Cookies.set('subscriptionjq', 'NO', { expires: 365 });{% comment %}/*Use evercookie to avoid problems when cookies are deleted*/{% endcomment %}
        var ec = new evercookie();{% comment %}/*set a cookie "id" to "12345"*/{% endcomment %}
        console.log("Setting cookie evercookie, subscribed -> NO");
        ec.set("subscription", "NO");
    }
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    </script>
    {% block page_js %}
    {% endblock %}
{% comment %}<!-- Google Tag Manager (noscript) -->{% endcomment %}<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5Z2PWFQ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>{% comment %}<!-- End Google Tag Manager (noscript) -->{% endcomment %}
    </body>
<html/>
