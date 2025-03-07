from django.shortcuts import redirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.db.models import Q
from system.models import ModuleMaster, MenuUrlMaster, ViewMenuUrlPermission

class PermissionMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if not request.session.get('is_authenticated', False):
            if request.path != '/':
                return redirect('login')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return None

        user_id = request.session.get('user_id')
        role_id = request.session.get('role_id')
        path_parts = request.path.strip('/').split('/')

        if len(path_parts) < 3:
            return None

        module_name, url, action = path_parts[:3]

        if action not in ['List', 'Save', 'Update', 'Close', 'Delete']:
            return None

        if not self.has_permission(module_name, user_id, role_id, url, action):
            message = f"You do not have permission to perform this action: {'view' if action == 'Close' else action}."
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Permission Denied</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f8d7da;
                    }}
                    .container {{
                        background: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(0,0,0,0.1);
                        text-align: center;
                    }}
                    h1 {{
                        color: #721c24;
                    }}
                    p {{
                        color: #721c24;
                    }}
                    a {{
                        display: inline-block;
                        margin-top: 20px;
                        padding: 10px 20px;
                        background-color: #007bff;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                    a:hover {{
                        background-color: #0056b3;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Forbidden (403)</h1>
                    <p>{message}</p>
                    <a href="javascript:window.history.back();">Go Back</a>
                </div>
            </body>
            </html>
            """
            return HttpResponse(html_content, status=403)

    def has_permission(self, module_name, user_id, role_id, url, action):
        action_permissions = {
            'List': 'is_list',
            'Save': 'is_save',
            'Update': 'is_update',
            'Close': 'is_close',
            'Delete': 'is_delete'
        }

        try:
            module = ModuleMaster.objects.get(name=module_name, status=1)
            menu = MenuUrlMaster.objects.get(url=url, module=module, status=1)
        except (ModuleMaster.DoesNotExist, MenuUrlMaster.DoesNotExist):
            return False

        permissions = ViewMenuUrlPermission.objects.filter(
            module_id=module.id,
            menu_id=menu.id,
            permisstion_status=1,
            permission_dtl_status=1
        ).filter(
            Q(role_id=role_id) | Q(user_id=user_id, role_id__isnull=True)
        )

        if action in action_permissions:
            permissions = permissions.filter(**{action_permissions[action]: True})

        return permissions.exists()
