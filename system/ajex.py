from pyexpat.errors import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from system.models import *

def get_parent_menus(request):
    if request.method == "POST":
        module_id = request.POST.get('module_id')
        if module_id:
            menus = MenuUrlMaster.objects.filter(
                module_id=module_id, status=1, parent_menu__isnull=True
            ).order_by('menu_name').values('id', 'menu_name')  
            menu_list = [{"id": menu["id"], "name": menu["menu_name"]} for menu in menus]
            return JsonResponse({"menus": menu_list}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_permissions(request):
    if request.method == "POST":
        permission_dict = {}
        module_id = request.POST.get("module_id")
        requestData = request.POST.get("requestData")
        
        role = RoleMaster.objects.filter(id=requestData).first()
        user = UserMaster.objects.filter(id=requestData).first()

        if not module_id or (not role and not user):
            return JsonResponse({"error": "Invalid module or role/user ID"}, status=400)

        # Fetch related menus for the selected module
        menus = MenuUrlMaster.objects.filter(module_id=module_id, parent_menu__isnull=False,status=1).order_by("menu_name")        
        role_permissions = list(ViewMenuUrlPermission.objects.filter(module_id=module_id, role_id=role.id,permisstion_status=1,permission_dtl_status=1) if role else [])
        user_permissions = list(ViewMenuUrlPermission.objects.filter(module_id=module_id, user_id=user.id,permisstion_status=1,permission_dtl_status=1) if user else [])
        existing_permissions = role_permissions + user_permissions
        if existing_permissions:
            permission_dict = {perm.menu_id: perm for perm in existing_permissions}
        permission_data = []
        for menu in menus:
            perm = permission_dict.get(menu.id)
            permission_data.append({
                "menu_id": menu.id,
                "menu_name": menu.menu_name,
                "parent_menu": menu.parent_menu.menu_name if menu.parent_menu else None,
                "url": menu.url,
                "is_save": perm.is_save if perm else False,
                "is_update": perm.is_update if perm else False,
                "is_close": perm.is_close if perm else False,
                "is_list": perm.is_list if perm else False,
                "is_delete": perm.is_delete if perm else False,
            })

        return JsonResponse({"permissions": permission_data}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)



def update_permission(request):
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        action = request.POST.get("action")
        is_checked = request.POST.get("is_checked") == "true"
        requestData = request.POST.get("requestData")
 
        role = RoleMaster.objects.filter(id=requestData).first()
        user = UserMaster.objects.filter(id=requestData).first()
   
        if not menu_id or not action or (not role and not user):
            return JsonResponse({"error": "Invalid data provided."}, status=400)

        permission, created = MenuUrlPermissionMaster.objects.get_or_create(
            menu_id=menu_id,
            module_id=request.POST.get("module_id"),
            role=role if role else None,
            user=user if user else None,
            status=1
        )

        permission_detail, created = MenuUrlPermissionDetails.objects.get_or_create(
            permission=permission,status=1
        )
   
        # Update the corresponding permission field
        if action == "save":
            permission_detail.is_save = is_checked
        elif action == "update":
            permission_detail.is_update = is_checked
        elif action == "close":
            permission_detail.is_close = is_checked
        elif action == "list":
            permission_detail.is_list = is_checked
        elif action == "delete":
            permission_detail.is_delete = is_checked

        permission_detail.save()
        return JsonResponse({"success": "Permission updated successfully."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=400)


