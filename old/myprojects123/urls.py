from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include("inventory.urls")),
    path('inventory-app/', include("inventory_app.urls")),
    path('system/', include("system.urls")),
]
