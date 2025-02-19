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
