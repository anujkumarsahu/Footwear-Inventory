from django.urls import path
from system import views
from django.conf import settings
from django.conf.urls.static import static
from system import ajex

urlpatterns = [
    path('dashboard',views.index,name="index"),
    path("role/<str:action>/<str:ids>",views.role,name="role"),
    path("user/<str:action>/<str:ids>",views.user,name="user"),
    path("module/<str:action>/<str:ids>",views.module,name="module"),
    path("menu/<str:action>/<str:ids>",views.menu,name="menu"),
    path("get_parent_menus/",ajex.get_parent_menus,name="get_parent_menus"),
    path("permissions/<str:action>/<str:ids>",views.permissions,name="permissions"),
    path("get_permission_list/",ajex.get_permissions,name="get_permission_list"),
    path("update_permission/",ajex.update_permission,name="update_permission"),
    path('change-module/<str:module_id>/', views.change_module, name='change_module'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# <div class="dropdown">
#     <button class="btn btn-primary dropdown-toggle" type="button" id="moduleDropdown" data-bs-toggle="dropdown" aria-expanded="false">
#         Select Module
#     </button>
#     <ul class="dropdown-menu" aria-labelledby="moduleDropdown">
#         {% for module in request.session.module_list %}
#             <li>
#                 <a class="dropdown-item d-flex align-items-center" href="#" onclick="changeModule('{{ module.id }}')">
#                     <img src="{{ module.image_url }}" alt="{{ module.name }}" class="module-icon me-2">
#                     {{ module.name }}
#                 </a>
#             </li>
#         {% endfor %}
#     </ul>
# </div>

# <script>
#     function changeModule(moduleId) {
#         window.location.href = "/change-module/" + moduleId + "/";
#     }
# </script>