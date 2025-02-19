from django.urls import path
from system import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path("role/<str:action>/<str:ids>",views.role,name="role"),
    path("user/<str:action>/<str:ids>",views.user,name="user"),
    path("module/<str:action>/<str:ids>",views.module,name="module"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

