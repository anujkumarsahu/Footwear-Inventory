import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import os

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=1)  

    class Meta:
        abstract = True
        db_table = 'tbl_base_model'
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
        managed = False

class Material(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tbl_material'
        managed = False

class Footwear(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    style_code = models.CharField(max_length=50, unique=True, blank=True)  # Make it blank initially
    category = models.ForeignKey(FootwearCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material)
    description = models.TextField()
    low_stock_threshold = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    
    class Meta:
        db_table = 'tbl_footwear'
        managed = False
    
    def save(self, *args, **kwargs):
        if not self.style_code:
            # Generate the style code
            name_part = self.name[:3].upper()  # First 3 characters of the name
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
            self.style_code = f"AK/{name_part}/{category_part}/{brand_part}/{sequential_number}"
        super().save(*args, **kwargs)

class FootwearImage(BaseModel):
    id = models.BigAutoField(primary_key=True)
    footwear = models.ForeignKey(Footwear, on_delete=models.CASCADE)
    image = models.ImageField( upload_to='footwear_images/',
      validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    # def save(self, *args, **kwargs):
    #     base_filename = self.footwear.name.replace(" ", "_")  
    #     existing_images_count = FootwearImage.objects.filter(footwear=self.footwear).count()
    #     ext = os.path.splitext(self.image.name)[1]
    #     new_image_name = f"{base_filename}_{existing_images_count + 1}{ext}"
    #     self.image.name = new_image_name
    #     super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.footwear.name} - Image {self.id}"
    
    class Meta:
        db_table = 'tbl_footwear_image'
        managed = False

class Size(BaseModel):
    SYSTEM_CHOICES = [
        ('EU', 'European'),
        ('UK', 'United Kingdom'),
        ('US', 'United States'),
        ('CM ', 'Centimeter')
    ]
    
    id = models.BigAutoField(primary_key=True)
    system = models.CharField(max_length=2, choices=SYSTEM_CHOICES)
    value = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ['system', 'value']

    def __str__(self):
        return f"{self.get_system_display()} {self.value}"
    
    class Meta:
        db_table = 'tbl_size'
        managed = False
        
        
class FootwearVariant(BaseModel):
    id = models.BigAutoField(primary_key=True)
    footwear = models.ForeignKey(Footwear, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['footwear', 'color', 'size']

    def __str__(self):
        return f"{self.footwear.name} - {self.color} - {self.size}"
    class Meta:
        db_table = 'tbl_footwear_variant'
        managed = False

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
    po_number = models.CharField(max_length=50, unique=True)
    po_date = models.DateField()
    expected_delivery = models.DateField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    class Meta:
        db_table = 'tbl_purchase'
        managed = False

class PurchaseDetail(BaseModel):
    id = models.BigAutoField(primary_key=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='details')
    variant = models.ForeignKey(FootwearVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    received_quantity = models.PositiveIntegerField(default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if self.received_quantity > self.quantity:
            raise ValidationError("Received quantity cannot exceed ordered quantity.")
        if self.received_quantity > 0:
            self.variant.stock_quantity += self.received_quantity
            self.variant.save()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'tbl_purchase_detail'
        managed = False

# Sales Management
class Customer(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tbl_customer'
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
    sale_date = models.DateField()
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.CharField(max_length=5, choices=PAYMENT_CHOICES)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.invoice_number
    class Meta:
        db_table = 'tbl_sale'
        managed = False
        
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            current_date = datetime.now().strftime('%Y%m%d')
            
            last_sale = Sale.objects.filter(status=1).order_by('id').last()
            
            if last_sale:
                last_sale_id = last_sale.id
                next_number = last_sale_id + 1
                # self.invoice_number = f"AK/{current_date}/{last_sale_id}"
            else:
                next_number =  1
            next_number_str = f"{next_number:06}"
            self.invoice_number = f"AK/{current_date}/{next_number_str}"

        super().save(*args, **kwargs)
        
class SaleDetail(BaseModel):
    id = models.BigAutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='details')
    variant = models.ForeignKey(FootwearVariant, on_delete=models.CASCADE)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.variant.stock_quantity < self.quantity:
            raise ValidationError("Insufficient stock for this variant.")
        self.variant.stock_quantity -= self.quantity
        self.variant.save()
        super().save(*args, **kwargs)
    class Meta:
        db_table = 'tbl_sale_detail'
        managed = False
        
# Return Management
class Return(BaseModel):
    RETURN_TYPE_CHOICES = [
        ('DMG', 'Damaged'),
        ('SIZ', 'Size Issue'),
        ('DEF', 'Defective'),
        ('OTH', 'Other')
    ]
    
    id = models.BigAutoField(primary_key=True)
    sale_detail = models.ForeignKey(SaleDetail, on_delete=models.CASCADE, related_name='returns')
    return_type = models.CharField(max_length=3, choices=RETURN_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.quantity > self.sale_detail.quantity:
            raise ValidationError("Returned quantity cannot exceed sold quantity.")
        self.sale_detail.variant.stock_quantity += self.quantity
        self.sale_detail.variant.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Return: {self.id} - {self.return_type}"
    
    class Meta:
        db_table = 'tbl_return'
        managed = False
        
# Promotions and Discounts
class Promotion(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    applicable_categories = models.ManyToManyField(FootwearCategory, related_name='promotions', blank=True)
    applicable_brands = models.ManyToManyField(Brand, related_name='promotions', blank=True)
    applicable_footwear = models.ManyToManyField(Footwear, related_name='promotions', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tbl_promotion'
        managed = False
# Expense Tracking
class ExpenseCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_expense_cateegory'
        managed = False
        
    def __str__(self):
        return self.name

class Expense(BaseModel):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    receipt = models.FileField(upload_to='expense_receipts/', null=True, blank=True)

    class Meta:
        db_table = 'tbl_expense'
        managed = False
    
    def __str__(self):
        return f"{self.category.name} - {self.date} - {self.amount}"