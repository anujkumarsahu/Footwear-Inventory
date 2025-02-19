import datetime
from django import forms
from .models import *

class FootwearCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FootwearCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = FootwearCategory
        fields = ['name', 'gender', 'description']

class BrandForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
        self.fields['description'] = forms.CharField(
            max_length=100, 
            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            required=True
        )
            
        self.fields['name'] = forms.CharField(
            max_length=100, 
            widget=forms.TextInput(attrs={'class': 'form-control', }),
            required=True
        )
            
        self.fields['logo'] = forms.ImageField(
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
            required=False
        )
    # class Meta:
    #     model = Brand
    #     fields = ['name', 'logo', 'description']

class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Material
        fields = ['name', 'description']

class GstMasterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GstMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
      
    class Meta:
        model = GstMaster
        fields = ['gst_type', 'gst_percentage']
        
        
class FootwearForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FootwearForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        choise_brand_list = [(k, v) for k, v in Brand.objects.filter(status=1).values_list('id', 'name').order_by('name')]
        choise_category_list = [(k, f'{v} - {n}') for k, v,n in FootwearCategory.objects.filter(status=1).values_list('id', 'name','gender').order_by('name')]
        # choise_material_list = [(k, v) for k, v in Material.objects.filter(status=1).values_list('id', 'name').order_by('name')]

        # self.fields['name'] = forms.CharField(
        #     max_length=100, 
        #     widget=forms.TextInput(attrs={'class': 'form-control'}), 
        #     required=True
        # )
        
        self.fields['category'] = forms.ChoiceField(
            choices=[('', '--Select--')] + choise_category_list,
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=True
        )
        
        self.fields['brand'] = forms.ChoiceField(
            choices=[('', '--Select--')] + choise_brand_list,
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=True
        )
        
        self.fields['description'] = forms.CharField(
            max_length=100, 
            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            required=False
        )
        
        # self.fields['materials'] = forms.ChoiceField(
        #     choices=[('', '--Select--')] + choise_material_list,
        #     widget=forms.Select(attrs={'class': 'form-control'}),
        #     required=True
        # )
        
        self.fields['low_stock_threshold'] = forms.CharField(
            widget=forms.NumberInput(attrs={'class': 'form-control'}), 
            required=True
        )

    # class Meta:
    #     model = Footwear
    #     fields = ['name', 'category', 'brand', 'materials', 'description', 'low_stock_threshold']

# class FootwearImageForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(FootwearImageForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'

#     class Meta:
#         model = FootwearImage
#         fields = ['footwear', 'image']

class SizeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Size
        fields = ['system', 'value']

class PurchaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        
        # Applying Bootstrap classes to all fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        # Choices for dropdown fields
        choise_supplier_list = [(k, v) for k, v in Supplier.objects.filter(status=1).values_list('id', 'name').order_by('name')]
        choise_materials_list = [(k, v) for k, v in Material.objects.filter(status=1).values_list('id', 'name').order_by('name')]
        choise_size_list = [(k, f'{v} - {n}') for k, v, n in Size.objects.filter(status=1).values_list('id', 'system', 'value').order_by('system')]
        choise_gst_list = [(k, f'{v} - {n}%') for k, v, n in GstMaster.objects.filter(status=1).values_list('id', 'gst_type', 'gst_percentage').order_by('gst_type')]
        choise_footwear_list = [
            (k, f"{v} - ({category_gender}) - {b:<20} ")
            for k, v, b,  category_gender in Footwear.objects.filter(status=1)
            .values_list('id', 'category__name', 'brand__name',  'category__gender')
            .order_by('id')
        ]
        # choise_footwear_list = [
        #     (k, f"{v} -({category_gender})\n {b:<20} {s:>20}")
        #     for k, v, b, s, category_gender in Footwear.objects.filter(status=1)
        #     .values_list('id', 'category__name', 'brand__name', 'style_code', 'category__gender')
        #     .order_by('id')
        # ]
        
        # Form fields for Purchase
        self.fields['po_number'] = forms.CharField(
            max_length=50,  required=True,  
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        self.fields['po_date'] = forms.DateField(
            required=True,
            widget=forms.DateInput(attrs={'class': 'form-control',"data-provide":"datepicker",'data-date-format':"dd-mm-yyyy" }),
            initial=datetime.datetime.today().date().strftime('%d-%m-%Y')
        )
        self.fields['supplier'] = forms.ChoiceField(
            choices=[('', '--Select--')] + choise_supplier_list,
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=True
        ) 
        choise_active_status_list = [('REC', 'Received'), ('PEN', 'Pending'),  ('PAR', 'Partially Received'),  ('CAN', 'Cancelled') ]
        self.fields['active_status'] = forms.ChoiceField(
            choices=choise_active_status_list,
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=True
        ) 
        
        self.fields['gst'] = forms.ChoiceField(
            choices=[('', '--Select--')] + choise_gst_list,
            widget=forms.Select(attrs={'class': 'form-control gst'}),
            required=False
        )
        self.fields['gst_amount'] = forms.DecimalField(
            max_digits=15,decimal_places=2,
            min_value=0,required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control gst_amount'})
        )
        self.fields['sub_total'] = forms.DecimalField(
            max_digits=15, decimal_places=2,  min_value=0,  required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control sub_total'})
        )
        self.fields['total_amount'] = forms.DecimalField(
            max_digits=15,  decimal_places=2, min_value=0,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control total_amount'})
        )
        self.fields['notes'] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        )

        # Form fields for FootwearVariant
        self.fields['footwear'] = forms.ChoiceField(
            choices=[('', '--Select--')] + choise_footwear_list,
            widget=forms.Select(attrs={'class': 'form-control select2 ', 'style': 'white-space: pre-wrap;'}),
            required=True
        )
         
        self.fields['materials'] = forms.ChoiceField(
            choices=[('', '--Select--')] + choise_materials_list,
            # choices= choise_materials_list,
            # widget=forms.Select(attrs={'class': 'select2 form-control select2-multiple ','multiple':"multiple"}),
            widget=forms.Select(attrs={'class': 'form-control select2 '}),
            required=True
        )
        self.fields['size'] = forms.ChoiceField(
            choices=[('', '--Select--')] + choise_size_list,
            widget=forms.Select(attrs={'class': 'form-control '}),
            required=True
        )
        self.fields['color'] = forms.CharField(
            max_length=50, required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        self.fields['name'] = forms.CharField(
            max_length=50, required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        # self.fields['color_code'] = forms.CharField(
        #     max_length=7,
        #     required=True,
        #     widget=forms.TextInput(attrs={'class': 'form-control' ,'id':"colorpicker-default"})
        # )
        
        self.fields['mrp'] = forms.DecimalField(
            max_digits=10, decimal_places=2,  min_value=0, required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )

        # Form fields for PurchaseDetail
        self.fields['quantity'] = forms.IntegerField(
            min_value=1,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control quantity'})
        )
        
        self.fields['p_price'] = forms.DecimalField(
            max_digits=10,
            decimal_places=2,
            min_value=0,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control p_price'})
        )
        self.fields['selling_price'] = forms.DecimalField(
            max_digits=10,
            decimal_places=2,
            min_value=0,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )

        # Form fields for FootwearImage
        self.fields['image'] = forms.ImageField(
            required=False,
            widget=forms.FileInput(attrs={'class': 'form-control-file'}),
        )


class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'contact_number', 'email', 'address', 'gst_number', 'payment_terms']



class CustomerForm(forms.ModelForm):
    contact_number = forms.CharField(min_length=10 ,max_length=10, required=True , widget=forms.TextInput(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer
        fields = ['name', 'contact_number', 'email', 'address']

class SaleForm(forms.Form):
    CHOICE_LIST = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('UPI', 'UPI'),
        ('MIXED', 'Mixed Payment')
    ]

    payable_amount = forms.DecimalField(
        max_digits=20, decimal_places=2, min_value=0, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    discount = forms.DecimalField(
        max_digits=20, decimal_places=2, min_value=0, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gst_amount = forms.DecimalField(
        max_digits=20, decimal_places=2, min_value=0, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    total_amount = forms.DecimalField(
        max_digits=20, decimal_places=2, min_value=0, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    payment_method = forms.ChoiceField(
        choices= CHOICE_LIST,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    notes = forms.CharField(
        max_length=200, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'})
    )

    gst = forms.ChoiceField(
        choices=[],  # This will be populated dynamically in __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)

        gst_choices = [('', '--Select--')] + [ (k, f"({s}) - {v}%") for k,s,v in GstMaster.objects.filter(status=1).values_list("id","gst_type", "gst_percentage").order_by('gst_type')]
        self.fields['gst'].choices = gst_choices

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        


