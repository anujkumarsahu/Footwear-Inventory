from decimal import Decimal
import os
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator,MinValueValidator, MaxValueValidator,MinLengthValidator



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=1)  

    class Meta:
        abstract = True
        db_table = 'tbl_base_model'
        app_label = 'inventory'
        managed = False

# Product Management
class FootwearCategory(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex'),
        ('K', 'Kids')
    ]
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['name', 'gender']

    def __str__(self):
        return f"{self.get_gender_display()} - {self.name}"
    class Meta:
        db_table = 'tbl_footwear_category'
        app_label = 'inventory'
        managed = False
      

class Brand(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tbl_brand'
        app_label = 'inventory'
        managed = False

class Material(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tbl_material'
        app_label = 'inventory'
        managed = False
        
class GstMaster(BaseModel):
    GST_TYPES = [
        ('SGST', 'SGST'),
        ('CGST', 'CGST'),
        ('IGST', 'IGST'),
        ('SGST+CGST', 'SGST & CGST'),
    ]
    gst_type = models.CharField(max_length=20, choices=GST_TYPES)
    gst_percentage = models.DecimalField(   max_digits=5, decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(100)]  )

    def __str__(self):
        return f"{self.gst_type} - {self.gst_percentage}%"
    class Meta:
        db_table = 'tbl_gst_mstr'
        app_label = 'inventory'
        managed = False
        

class Footwear(BaseModel):
    id = models.BigAutoField(primary_key=True)
    # name = models.CharField(max_length=200)
    style_code = models.CharField(max_length=100, unique=True, blank=True)  # Make it blank initially
    category = models.ForeignKey(FootwearCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    low_stock_threshold = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.brand.name} - {self.style_code}"
    
    class Meta:
        db_table = 'tbl_footwear'
        app_label = 'inventory'
        managed = False
        
    
    def save(self, *args, **kwargs):
        if not self.style_code:
            # Generate the style code
            category_part = self.category.name[:3].upper()  # First 3 characters of the category name
            brand_part = f"{self.brand.name[0].upper()}{self.brand.name[-1].upper()}"  # First and last character of the brand name
            
            # Get the next sequential number
            last_footwear = Footwear.objects.order_by('id').last()
            if last_footwear:
                next_number = last_footwear.id + 1
            else:
                next_number = 1
            sequential_number = f"{next_number:06}"  # 6 digits with leading zeros
            # Combine all parts to form the style code
            self.style_code = f"AK/{category_part}/{brand_part}/{sequential_number}"
        super().save(*args, **kwargs)



# Supplier Management
class Supplier(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    gst_number = models.CharField(max_length=15, unique=True)
    payment_terms = models.PositiveIntegerField(help_text="Payment terms in days")

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tbl_supplier'
        app_label = 'inventory'
        managed = False
        
        
class Size(BaseModel):
    SYSTEM_CHOICES = [
        ('EU', 'European - (EU)'),
        ('UK', 'United Kingdom - (UK)'),
        ('US', 'United States - (US)'),
        ('CM ', 'Centimeter - (CM)')
    ]
    
    id = models.BigAutoField(primary_key=True)
    system = models.CharField(max_length=5, choices=SYSTEM_CHOICES)
    value = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ['system', 'value']

    def __str__(self):
        return f"{self.get_system_display()} {self.value}"
    
    class Meta:
        db_table = 'tbl_size'
        app_label = 'inventory'
        managed = False
        
        

class Purchase(BaseModel):
    STATUS_CHOICES = [
        ('PEN', 'Pending'),
        ('REC', 'Received'),
        ('PAR', 'Partially Received'),
        ('CAN', 'Cancelled')
    ]
    
    id = models.BigAutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    gst = models.ForeignKey(GstMaster, on_delete=models.CASCADE,null=True, blank=True)
    gst_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    po_number = models.CharField(max_length=50, unique=True)
    po_date = models.DateField()
    active_status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='REC')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    class Meta:
        db_table = 'tbl_purchase'
        app_label = 'inventory'
        managed = False
        
      
class FootwearVariant(BaseModel):
    id = models.BigAutoField(primary_key=True)
    footwear = models.ForeignKey(Footwear, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    p_price = models.DecimalField(max_digits=15, decimal_places=2)
    # selling_price = models.DecimalField(max_digits=15, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        unique_together = ['footwear', 'color', 'size']
        
    def save(self, *args, **kwargs):
        # Update stock quantity before saving
        if not self.pk:  # Only update stock_quantity if it's a new object
            self.stock_quantity += self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.footwear.category.name} - {self.color} - {self.size}"
    class Meta:
        db_table = 'tbl_footwear_variant'
        app_label = 'inventory'
        managed = False
        
        
  





# Sales Management
class Customer(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    contact_number = models.CharField(validators=[MinLengthValidator(10)], max_length=10, unique=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
   
    def __str__(self):
        return self.contact_number
    
    class Meta:
        db_table = 'tbl_customer'
        app_label = 'inventory'
        managed = False
        

class Sale(BaseModel):
    PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('UPI', 'UPI'),
        ('MIXED', 'Mixed Payment')
    ]

    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='sales')
    invoice_number = models.CharField(max_length=50, unique=True)
    sale_date = models.DateField(auto_now_add=False)
    payable_amount = models.DecimalField(max_digits=15, decimal_places=2)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    gst = models.ForeignKey(GstMaster, on_delete=models.SET_NULL, null=True, blank=True)
    gst_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='CASH')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Invoice: {self.invoice_number}"

    class Meta:
        db_table = 'tbl_sale'
        app_label = 'inventory'
        managed = False
        


class SaleDetail(BaseModel):
    id = models.BigAutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_details')
    variant = models.ForeignKey(FootwearVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total_price = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return f"Sale : {self.sale.invoice_number} - Variant: {self.variant} - Qty: {self.quantity}"

    class Meta:
        db_table = 'tbl_sale_detail'
        app_label = 'inventory'
        managed = False
        
    

        
# # Return Management
# class Return(BaseModel):
#     RETURN_TYPE_CHOICES = [
#         ('DMG', 'Damaged'),
#         ('SIZ', 'Size Issue'),
#         ('DEF', 'Defective'),
#         ('OTH', 'Other')
#     ]
    
#     id = models.BigAutoField(primary_key=True)
#     sale_detail = models.ForeignKey(SaleDetail, on_delete=models.CASCADE,)
#     return_type = models.CharField(max_length=3, choices=RETURN_TYPE_CHOICES)
#     quantity = models.PositiveIntegerField()
#     notes = models.TextField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if self.quantity > self.sale_detail.quantity:
#             raise ValidationError("Returned quantity cannot exceed sold quantity.")
#         self.sale_detail.variant.stock_quantity += self.quantity
#         self.sale_detail.variant.save()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Return: {self.id} - {self.return_type}"
    
#     class Meta:
#         db_table = 'tbl_return'
#         app_label = 'inventory'
#         managed = False
        
        
# Promotions and Discounts
class Promotion(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    applicable_categories = models.ManyToManyField(FootwearCategory,  blank=True)
    applicable_brands = models.ManyToManyField(Brand,  blank=True)
    applicable_footwear = models.ManyToManyField(Footwear,  blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tbl_promotion'
        app_label = 'inventory'
        managed = False
        
# Expense Tracking
class ExpenseCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_expense_cateegory'
        app_label = 'inventory'
        managed = False
        
    def __str__(self):
        return self.name

class Expense(BaseModel):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE,)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    receipt = models.FileField(upload_to='expense_receipts/', null=True, blank=True)

    class Meta:
        db_table = 'tbl_expense'
        app_label = 'inventory'
        managed = False
        
    
    def __str__(self):
        return f"{self.category.name} - {self.date} - {self.amount}"