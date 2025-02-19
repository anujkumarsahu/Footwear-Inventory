from django.urls import path
from system123 import views
urlpatterns = [
    path("",views.index,name="index")
]
