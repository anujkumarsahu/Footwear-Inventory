from django import forms
from system.models import *

class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RoleMaster
        fields = ('name','description',)
        
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        self.fields['role'] = forms.ModelChoiceField(
            queryset=RoleMaster.objects.filter(status=1).order_by('name'),
            empty_label="Select",
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    class Meta:
        model = UserMaster
        fields = ('name', 'role', 'email', 'password', 'mobile_no', 'address', 'upload_file')

        widgets = {
            'upload_file': forms.ClearableFileInput(),
            'address': forms.Textarea(attrs={'rows': '2'}),  
        }



class ModuleMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModuleMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = ModuleMaster
        fields = ['name','db_name','description','db_schema_name','db_pass','module_img']
        widgets = {
            'module_img': forms.ClearableFileInput(),
        }


class MenuUrlMasterForm(forms.ModelForm):
    url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    menu_icon = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '<i class="bx bx-home-circle"></i>'}))

    class Meta:
        model = MenuUrlMaster
        fields = ['menu_name', 'url', 'module', 'parent_menu', 'is_toolbar', 'order_no', 'clear_query', 'menu_icon']

        widgets = {
            'menu_name': forms.TextInput(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'parent_menu': forms.Select(attrs={'class': 'form-control'}),
            'is_toolbar': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': "width: 40px; height: 20px; cursor: pointer;"}),
            'order_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'clear_query': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super(MenuUrlMasterForm, self).__init__(*args, **kwargs)
        
        # Set the default choice for parent_menu
        self.fields['parent_menu'].choices = [('', 'Self')] 
        # self.fields['parent_menu'].choices = [('', 'Self')] + list(MenuUrlMaster.objects.filter(status=1).values_list('id', 'menu_name').order_by('menu_name'))



class MenuUrlPermissionMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuUrlPermissionMasterForm, self).__init__(*args, **kwargs)

        # Setting Querysets and Empty Labels for ForeignKey Fields
        self.fields['module'].queryset = ModuleMaster.objects.filter(status=1).order_by('name')
        self.fields['module'].empty_label = "--Please Select--"

        self.fields['role'].queryset = RoleMaster.objects.filter(status=1).order_by('name')
        self.fields['role'].empty_label = "--Please Select--"

        self.fields['user'].queryset = UserMaster.objects.filter(status=1).order_by('name')
        self.fields['user'].empty_label = "--Please Select--"

    class Meta:
        model = MenuUrlPermissionMaster
        fields = ['module', 'user', 'role']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    