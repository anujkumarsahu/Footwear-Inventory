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

from django import forms
from .models import ModuleMaster, MenuUrlMaster

class MenuUrlMasterForm(forms.Form):
    menu_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    url = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    module = forms.ModelChoiceField(
        queryset=ModuleMaster.objects.filter(status=1).order_by('name'),
        empty_label="Select",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    parent_menu = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    is_toolbar = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': "width: 40px; height: 20px; cursor: pointer;"})
    )

    order_no = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    clear_query = forms.CharField(
        initial="cmd=clear",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
    )

    menu_icon = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '<i class="bx bx-home-circle"></i>'})
    )

    def __init__(self, *args, **kwargs):
        super(MenuUrlMasterForm, self).__init__(*args, **kwargs)

        choice_list = [(k, v) for k, v in MenuUrlMaster.objects.filter(status=1).values_list('id', 'menu_name').order_by('menu_name')]
        self.fields['parent_menu'].choices = [('', 'Self')] + choice_list
