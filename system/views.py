from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from system.models import *
from system.forms import *
from django.db.models import Q
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

def logout(request):
    request.session.flush() 
    messages.success(request, 'Logged out successfully .')
    return redirect('login')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            try:
                user_master = get_object_or_404(UserMaster, email=email, status=1)

                if password != user_master.password:
                    messages.error(request, 'Invalid credentials!')
                    return redirect('login')

                request.session.update({
                    'is_authenticated': True,
                    'user_id': user_master.id,
                    'role_id': user_master.role.id if user_master.role else None,
                    'role_name': user_master.role.name if user_master.role else None,
                    'user_name': user_master.name,
                })

                role_id = user_master.role.id if user_master.role else None

                module_ids = set(ViewMenuUrlPermission.objects.filter( permisstion_status=1
                ).filter( Q(role_id=role_id) | Q(user_id=user_master.id, role_id__isnull=True) ).values_list('module_id', flat=True))
                modules = list(ModuleMaster.objects.filter(id__in=module_ids, status=1).order_by('id'))

                if modules:
                    module_first = modules[0]
                    
                    request.session.update({
                        'module_id': module_first.id,
                        'module_name': module_first.name,
                        'module_img': module_first.module_img.url,
                        'module_list': [
                            {
                                'id': module.id,
                                'name': module.name,
                                'module_img': module.module_img.url if module.module_img else None 
                            } 
                            for module in modules
                        ],
                    })
                    update_menu_structure(request, module_first.id, role_id, user_master.id)
                    first_menu_url = get_first_menu_url(module_first.id, role_id, user_master.id)

                    if first_menu_url:
                        return redirect(first_menu_url)
                    else:
                        messages.error(request, "No accessible pages found for your role.")
                        return redirect('login')

                # return redirect(menu_structure.)

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, f'Please Enter valid Email!')
    return render(request, 'sys_master/login.html')

def get_first_menu_url(module_id, role_id, user_id):
    """
    Get the first accessible menu URL (index page) for the given module, role, and user.
    Prioritizes menus with is_list=True.
    """
    permission = ViewMenuUrlPermission.objects.filter(
    module_id=module_id,permisstion_status=1, is_list=True ).filter( Q(role_id=role_id) | Q(user_id=user_id)
    ).first()
    if permission:
        try:
            menu = MenuUrlMaster.objects.get(id=permission.menu_id)
            return menu.url 
        except MenuUrlMaster.DoesNotExist:
            return None

    return None

def update_menu_structure(request, module_id, role_id, user_id):
    """ Updates the session with menu structure based on module selection. """
    permissions = ViewMenuUrlPermission.objects.filter(
        module_id=module_id, permisstion_status=1, permission_dtl_status=1,  is_list=True,
    ).filter( Q(role_id=role_id) | Q(user_id=user_id, role_id__isnull=True) )
   
    parent_menu_ids = list(permissions.values_list('parent_menu_id', flat=True))
    child_menu_ids = list(permissions.values_list('menu_id', flat=True))

    parent_menus = {
        menu.id: menu for menu in MenuUrlMaster.objects.filter(id__in=parent_menu_ids)
    }
    child_menus = list(MenuUrlMaster.objects.filter(id__in=child_menu_ids))

    menu_structure = {
        p_id: {'name': menu.menu_name, 'icon': menu.menu_icon, 'order_no': menu.order_no, 'children': []}
        for p_id, menu in parent_menus.items()
    }

    for child in child_menus:
        if child.parent_menu and child.parent_menu.id in menu_structure:
            menu_structure[child.parent_menu.id]['children'].append({
                'name': child.menu_name,
                'url': child.url,
                'clear_query': child.clear_query,
                'action': 'List',
                'ids': None,
                'order_no': child.order_no
            })

    request.session['menu_structure'] = menu_structure


def change_module(request, module_id):
    """ Changes the active module and updates session with new menus. """
    if not request.session.get('is_authenticated', False):
        return redirect('login')

    role_id = request.session.get('role_id')
    user_id = request.session.get('user_id')

    module = get_object_or_404(ModuleMaster, id=module_id, status=1)

    # Store the image URL instead of FieldFile object
    module_img_url = module.module_img.url if module.module_img else ""

    request.session.update({
        'module_id': module.id,
        'module_name': module.name,
        'module_img': module_img_url, 
    })

    update_menu_structure(request, module.id, role_id, user_id)
    first_menu_url = get_first_menu_url(module.id, role_id, user_id)

    if first_menu_url:
        return redirect(first_menu_url)
    else:
        messages.error(request, "No accessible pages found for your role.")
        return redirect('login')


def index (request):
    return render(request, 'sys_master/index.html')    


def role(request, action, ids=None):
    role_list = None
    form = RoleForm()

    if action == "Save":
        if request.method == 'POST':
            form = RoleForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                
                if not RoleMaster.objects.filter(name=name, status=1).exists():
                    RoleMaster.objects.create(name=name, description=description)
                    messages.success(request, "Data successfully created.")
                    return redirect('role', 'Save', None)
                else:
                    messages.error(request, 'Data Already Exists.')
            else:
                messages.error(request, 'Form Not Valid.')

    elif action == 'Update' and ids:
        ids = int(ids)
        role_ins = get_object_or_404(RoleMaster, id=ids)
        form = RoleForm(instance=role_ins) 

        if request.method == 'POST':
            form = RoleForm(request.POST, instance=role_ins)  #
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']

                if not RoleMaster.objects.filter(name=name, status=1).exclude(id=ids).exists():
                    form.save()  
                    messages.success(request, 'Data Successfully Updated.')
                    return redirect('role', 'List', None)
                else:
                    messages.error(request, 'Data Already Exists.')
            else:
                messages.error(request, 'Form Not Valid. Please check the errors below.')

    elif action == "Close" and ids:
        ids = int(ids)
        role_ins = get_object_or_404(RoleMaster, id=ids)
        form = RoleForm(instance=role_ins)

        for visible in form.visible_fields():
            visible.field.widget.attrs['disabled'] = True

        if request.method == 'POST':
            return redirect('role', 'List', None)

    elif action == "List":
        role_list = RoleMaster.objects.filter(status=1).order_by('-id')

        if request.method == 'POST':
            if 'DelData' in request.POST:
                DelData = request.POST['DelData']
                RoleMaster.objects.filter(id=DelData).update(status=0)
                messages.error(request, 'Data Successfully Deactivated.')
            elif 'ActData' in request.POST:
                ActData = request.POST['ActData']
                RoleMaster.objects.filter(id=ActData).update(status=1)
                messages.success(request, 'Data Successfully Activated.')

    template = "sys_master/role_list.html" if action == 'List' else "sys_master/role.html"
    context = {'action': action, 'form': form, 'role_list': role_list}
    
    return render(request, template, context)


def user(request, action, ids=None):
    user_list = None
    form = UserForm()

    if action == "Save":
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                mobile_no = form.cleaned_data['mobile_no'] 

                if str(mobile_no).isdigit() and len(str(mobile_no)) == 10:  
                    if not UserMaster.objects.filter(mobile_no=mobile_no, status=1).exists():
                        form.save()
                        messages.success(request, "User successfully created.")
                        return redirect('user', 'Save', None)
                    else:
                        messages.error(request, 'User with this mobile number already exists.')
                else:
                    messages.error(request, 'User mobile number must be exactly 10 digits long and contain only numbers.')
            else:
                messages.error(request, 'Invalid form submission. Please check the errors.')
  

    elif action == 'Update' and ids:
        user_instance = get_object_or_404(UserMaster, id=ids)
        form = UserForm(instance=user_instance)

        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES, instance=user_instance)
            if form.is_valid():
                mobile_no = form.cleaned_data['mobile_no']
                
                if str(mobile_no).isdigit() and len(str(mobile_no)) == 10:   
                    if not UserMaster.objects.filter(mobile_no=mobile_no, status=1).exclude(id=ids).exists():
                        form.save()
                        messages.success(request, 'User details successfully updated.')
                        return redirect('user', 'List',None)
                    else:
                        messages.error(request, 'Another user with this mobile number already exists.')
                else:
                    messages.error(request, 'User mobile number must be exactly 10 digits long and contain only numbers.')
            else:
                messages.error(request, 'Invalid form submission. Please check the errors.')
  
    elif action == "Close" and ids:
        user_instance = get_object_or_404(UserMaster, id=ids)
        form = UserForm(instance=user_instance)

        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True

        if request.method == 'POST':
            return redirect('user', 'List',None)

    elif action == "List":
        user_list = UserMaster.objects.filter(status=1).order_by('-id')

        if request.method == 'POST':
            if 'DelData' in request.POST:
                user_id = request.POST['DelData']
                UserMaster.objects.filter(id=user_id).update(status=0)
                messages.success(request, 'User successfully deactivated.')
            elif 'ActData' in request.POST:
                user_id = request.POST['ActData']
                UserMaster.objects.filter(id=user_id).update(status=1)
                messages.success(request, 'User successfully activated.')

    template = "sys_master/user_list.html" if action == 'List' else "sys_master/user.html"
    context = {'action': action, 'form': form, 'user_list': user_list}

    return render(request, template, context)


def module(request, action, ids=None):
    module_list = None
    form = ModuleMasterForm()

    if action == "Save":
        if request.method == 'POST':
            form = ModuleMasterForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data['name'].lower()
                user = UserMaster.objects.filter(status=1).first() 

                if not ModuleMaster.objects.filter(name=name, status=1).exists():
                    module_instance = form.save(commit=False)  
                    module_instance.user = user 
                    module_instance.save()
                    messages.success(request, "Module successfully created.")
                    return redirect('module', 'List', None)
                else:
                    messages.error(request, 'Module with this name already exists.')

    elif action == 'Update' and ids:
        module_instance = get_object_or_404(ModuleMaster, id=ids)
        form = ModuleMasterForm(instance=module_instance)

        if request.method == 'POST':
            form = ModuleMasterForm(request.POST, request.FILES, instance=module_instance)
            if form.is_valid():
                name = form.cleaned_data['name'].lower()
                user = UserMaster.objects.filter(status=1).first()  

                if not ModuleMaster.objects.filter(name=name, status=1).exclude(id=ids).exists():
                    module_instance = form.save(commit=False)
                    module_instance.user = user 
                    module_instance.save()
                    messages.success(request, "Module successfully updated.")
                    return redirect('module', 'List', None)
                else:
                    messages.error(request, 'Module with this name already exists.')

    elif action == "Close" and ids:
        module_instance = get_object_or_404(ModuleMaster, id=ids)
        form = ModuleMasterForm(instance=module_instance)

        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True

        if request.method == 'POST':
            return redirect('module', 'List', None)

    elif action == "List":
        module_list = ModuleMaster.objects.filter(status=1).order_by('-id')

        if request.method == 'POST':
            if 'DelData' in request.POST:
                ids = request.POST['DelData']
                ModuleMaster.objects.filter(id=ids).update(status=0)
                messages.success(request, "Module successfully deactivated.")
            elif 'ActData' in request.POST:
                ids = request.POST['ActData']
                ModuleMaster.objects.filter(id=ids).update(status=1)
                messages.success(request, "Module successfully activated.")

    template = "sys_master/module_list.html" if action == 'List' else "sys_master/module.html"
    context = {'action': action, 'form': form, 'module_list': module_list}

    return render(request, template, context)



def menu(request, action, ids=None):
    menu_list = None
    form = MenuUrlMasterForm()

    if action == "Save":
        if request.method == 'POST':
            print("request:",request.POST)
            form = MenuUrlMasterForm(request.POST)
            if form.is_valid():
                menu_name = form.cleaned_data['menu_name']
                module = form.cleaned_data['module']
                user = UserMaster.objects.filter(status=1).first()  

                if not MenuUrlMaster.objects.filter(menu_name=menu_name,module_id = module, status=1).exists():
                    menu_instance = form.save(commit=False)
                    menu_instance.user = user
                    menu_instance.save()
                    messages.success(request, "Menu successfully created.")
                    return redirect('menu', 'List', None)  
                else:
                    messages.error(request, 'Menu with this name already exists.')

    elif action == 'Update' and ids:
        menu_instance = get_object_or_404(MenuUrlMaster, id=ids)
        form = MenuUrlMasterForm(instance=menu_instance)

        if request.method == 'POST':
            form = MenuUrlMasterForm(request.POST, instance=menu_instance)
            if form.is_valid():
                menu_name = form.cleaned_data['menu_name']
                module = form.cleaned_data['module']
                if not MenuUrlMaster.objects.filter(menu_name=menu_name,module_id = module, status=1).exclude(id=ids).exists():
                    menu_instance = form.save(commit=False)
                    menu_instance.save()
                    messages.success(request, "Menu successfully updated.")
                    return redirect('menu', 'List',None)
                else:
                    messages.error(request, 'Menu with this name already exists.')

    # Close (View Only) Menu
    elif action == "Close" and ids:
        menu_instance = get_object_or_404(MenuUrlMaster, id=ids)
        form = MenuUrlMasterForm(instance=menu_instance)

    
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True

        if request.method == 'POST':
            return redirect('menu', 'List',None)

    # List all menus
    elif action == "List":
        menu_list = MenuUrlMaster.objects.all().order_by('-id')

        if request.method == 'POST':
            if 'DelData' in request.POST:
                ids = request.POST['DelData']
                MenuUrlMaster.objects.filter(id=ids).update(status=0)
                messages.success(request, "Menu successfully deactivated.")
            elif 'ActData' in request.POST:
                ids = request.POST['ActData']
                MenuUrlMaster.objects.filter(id=ids).update(status=1)
                messages.success(request, "Menu successfully activated.")

    template = "sys_master/menu_list.html" if action == 'List' else "sys_master/menu.html"
    
    context = {'action': action, 'form': form, 'menu_list': menu_list}
    return render(request, template, context)


def permissions(request,action,ids=None):
    user_list = role_list = module_list = None
    template = "sys_master/menu_url_permisstions.html" 
    user_list = UserMaster.objects.filter(status=1).values('id','name').order_by('name')
    role_list = RoleMaster.objects.filter(status=1).values('id','name').order_by('name')
    module_list = ModuleMaster.objects.filter(status=1).values('id','name').order_by('name')
    context = {'user_list':user_list,'role_list':role_list,'module_list':module_list}
    return render(request, template, context)

