from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('app',views.app,name='app'),
    path('about',views.about,name='about'),
    path('search',views.search,name='search'),
    path('aircompressor',views.aircompressor,name='aircompressor'),
    path('machinetools',views.machinetools,name='machinetools'),
    path('powertools',views.powertools,name='powertools'),
    path('contact',views.contact,name='contact'),
    path('index',views.index,name='index'),
    path('',views.login_view,name=''),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout_view,name='logout'),
    path('footer',views.footer,name='footer'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('cart',views.cart,name='cart'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('description/<pk>',views.description,name='description'),
    path('remove_from_cart',views.remove_from_cart,name='remove_from_cart'),
    path('checkout',views.checkout,name='checkout'),
    path('placeorder',views.shipping_info,name='placeorder'),
    path('payment',views.payment,name='payment'),







]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)