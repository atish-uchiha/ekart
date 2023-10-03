from django.urls import path
from storeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('contact',views.contact),
    path('about',views.about),
    path('delete/<rid>',views.delete),
    path('edit/<rid>',views.edit),   
    path('greet',views.greet), 
    path('addproduct',views.addproduct),
    path('index',views.index),
    path('details/<id>',views.details),
    path('cart',views.viewcart),
    path('login',views.user_login),
    path('register',views.register),
    path('catfilter/<cv>',views.catfilter),
    path('pricerange',views.pricerange),
    path('sort/<sv>',views.sort),
    path('logout',views.user_logout),
    path('addcart/<rid>',views.addcart),
    path('remove/rid',views.removecart),
    path('qty/<sig>/<pid>',views.cartqty),
    path('placeorder',views.place_order),
    path('payment',views.payment),
    path('sendmail',views.sendmail),
    path('message',views.mailmsg),
    path('entermail',views.entermail),
    path('enterotp',views.enterotp),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)