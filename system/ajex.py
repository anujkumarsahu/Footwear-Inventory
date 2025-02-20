from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from system.models import *


def get_parent_menus(request):
    if request.method == "POST":
        module_id = request.POST.get('module_id')
        if module_id:
            menus = MenuUrlMaster.objects.filter(module_id=module_id, status=1, parent_menu__isNull=True).order_by('menu_name')
            menu_list = [{"id": menu.id, "name": menu.menu_name} for menu in menus]
            return JsonResponse({"menus": menu_list}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)