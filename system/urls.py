from django.urls import path
from system import views
from django.conf import settings
from django.conf.urls.static import static
from system import ajex

urlpatterns = [
    path('',views.index,name="index"),
    path("role/<str:action>/<str:ids>",views.role,name="role"),
    path("user/<str:action>/<str:ids>",views.user,name="user"),
    path("module/<str:action>/<str:ids>",views.module,name="module"),
    path("menu/<str:action>/<str:ids>",views.menu,name="menu"),
    path("get_parent_menus/",ajex.get_parent_menus,name="get_parent_menus"),
    path("permissions/",views.permissions,name="permissions"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

