from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from inventory import views
from inventory import ajax
urlpatterns = [
    path("",views.index,name="index"),
    path("footwear/<str:action>/<str:ids>",views.footwear,name="footwear"),
    path("purchase/<str:action>/<str:ids>",views.purchase,name="purchase"),
    path("sale/<str:action>/<str:ids>",views.sale,name="sale"),
    path('get_footwear_sizes/', ajax.get_footwear_sizes, name='get_footwear_sizes'),
    path('get-gst-percentage/', ajax.get_gst_percentage, name='get_gst_percentage'),

     
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 