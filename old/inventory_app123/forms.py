from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
        self.fields['sku']=forms.CharField(widget=forms.TextInput(attrs={'class': "form-control-input"}), required=True)
        self.fields['description']=forms.CharField(widget=forms.TextInput(attrs={'class': "form-control-input"}), required=True)
        
        choice1 = {k: f'{v} - ({n})' for k, v, n in GstMaster.objects.filter(status=1).values_list('id', 'gst_type','gst_percentage').order_by('gst_type')}
        gst_list = list(choice1.items())
        self.fields['gst'] = forms.ChoiceField(widget=forms.Select( attrs={'class': 'form-control-input'}), choices=[('', 'Please Select')] + gst_list, required=False)
        
        choice1 = {k: v for k, v in Brand.objects.filter(status=1).values_list('id', 'name').order_by('name')}
        brand_list = list(choice1.items())
        self.fields['brand'] = forms.ChoiceField(widget=forms.Select( attrs={'class': 'form-control-input'}), choices=[('', 'Please Select')] + brand_list, required=False)
        
        choice1 = {k: v for k, v in Category.objects.filter(status=1).values_list('id', 'name').order_by('name')}
        category_list = list(choice1.items())
        self.fields['category'] = forms.ChoiceField(widget=forms.Select( attrs={'class': 'form-control-input'}), choices=[('', 'Please Select')] + category_list, required=False)
        
        choice1 = {k: v for k, v in Color.objects.filter(status=1).values_list('id', 'name').order_by('name')}
        color_list = list(choice1.items())
        self.fields['color'] = forms.ChoiceField(widget=forms.Select( attrs={'class': 'form-control-input'}), choices=[('', 'Please Select')] + color_list, required=False)
        
        choice1 = {k: f'{v} - ({n})' for k, v, n in Size.objects.filter(status=1).values_list('id', 'size_type','value').order_by('size_type')}
        size_list = list(choice1.items())
        self.fields['size'] = forms.ChoiceField(widget=forms.Select( attrs={'class': 'form-control-input'}), choices=[('', 'Please Select')] + size_list, required=True)

    class Meta:
        model = Product
        fields = ['sku','brand','category','color','size','gst','description']

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
            
        self.fields['name']=forms.CharField(widget=forms.TextInput(attrs={'class': "form-control-input"}), required=True)
        self.fields['contact_no']=forms.CharField(max_length=10,min_length=10,widget=forms.NumberInput(attrs={'class': "form-control-input"}), required=True)
        self.fields['email']=forms.EmailField(widget=forms.EmailField(attrs={'class': "form-control-input"}), required=True)
        self.fields['gst_number']=forms.CharField(max_length=16,widget=forms.TextInput(attrs={'class': "form-control-input"}), required=True)
        self.fields['address']=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': "form-control-input"}), required=True)

    class Meta:
        model = Supplier
        fields = ('name','contact_no','email','gst_number','address')

class BrandForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
        
        self.fields['name']= forms.CharField( max_length=100,widget=forms.TextInput(attrs={'class':'form-control-input'}), required=True)
        
        
    class Meta:
        model = Brand
        fields = ("name",)
        
class SizeTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SizeTypeForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
        
        self.fields['name']= forms.CharField( max_length=20,widget=forms.TextInput(attrs={'class':'form-control-input'}), required=True)
        
        
    class Meta:
        model = SizeType
        fields = ("name",)


class SizeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
            
        self.fields['value']= forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control-input'}), required=True)
        choice1 = {k: v for k, v in SizeType.objects.filter(status=1).values_list('id', 'name').order_by('name')}
        size_type_list = list(choice1.items())
        self.fields['size_type'] = forms.ChoiceField(widget=forms.Select( attrs={'class': 'form-control-input'}), choices=[('', 'Please Select')] + size_type_list, required=True)

    class Meta:
        model = Size
        fields = ('size_type','value',)
        
class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
            
        self.fields['name']= forms.CharField( max_length=100,widget=forms.TextInput(attrs={'class':'form-control-input'}), required=True)
        
        choice1 = {k: v for k, v in ProductGenderCategory.objects.filter(status=1).values_list('id', 'name').order_by('name')}
        product_gender_list = list(choice1.items())
        self.fields['product_gender'] = forms.ChoiceField(widget=forms.Select( attrs={'class': 'form-control-input'}), choices=[('', 'Please Select')] + product_gender_list, required=True)

    class Meta:
        model = Category
        fields = ('product_gender','name',)


class ColorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ColorForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
            
        self.fields['name'] = forms.CharField( max_length=30, widget=forms.TextInput(attrs={'class':'form-control-input'}),required=True)
    

    class Meta:
        model = Color
        fields = ('name',)
        


class GstMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ColorForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control-input'
            
        self.fields['gst_type'] = forms.CharField( max_length=30, widget=forms.TextInput(attrs={'class':'form-control-input'}),required=True)
        self.fields['gst_percentage'] = forms.CharField(min_length=0 ,max_length=20, widget=forms.NumberInput(attrs={'class':'form-control-input'}),required=True)
    

    class Meta:
        model = GstMaster
        fields = ('gst_type','gst_percentage')