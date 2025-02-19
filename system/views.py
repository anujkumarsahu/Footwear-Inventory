from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from system.models import *
from system.forms import *

# Create your views here.

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
                name = form.cleaned_data['name']
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
                name = form.cleaned_data['name']
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

