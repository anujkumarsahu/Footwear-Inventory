from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)
    status = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True


class Supplier(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    contact_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    gst_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name



class Customer(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    contact_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductGenderCategory(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    id = models.BigAutoField(primary_key=True)
    product_gender = models.ForeignKey(ProductGenderCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.product_gender.name} - {self.name}"

class Color(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SizeType(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Size(BaseModel):
    id = models.BigAutoField(primary_key=True)
    size_type = models.ForeignKey(SizeType, on_delete=models.CASCADE)
    value = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.size_type.name} - {self.value}"

class GstMaster(BaseModel):
    id = models.BigAutoField(primary_key=True)
    gst_type = models.CharField(max_length=50, choices=[('IGST', 'IGST'), ('SGST + CGST', 'SGST + CGST')])
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2)

class Product(BaseModel):
    id = models.BigAutoField(primary_key=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.sku}"

# Stock Management



# Purchase System
class Purchase(BaseModel):
    id = models.BigAutoField(primary_key=True)
    invoice = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    gst = models.ForeignKey(GstMaster, on_delete=models.CASCADE)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    

    def __str__(self):
        return f"PO #{self.id} - {self.supplier.name}"


class PurchaseDetail(BaseModel):
    id = models.BigAutoField(primary_key=True)
    product_model = models.CharField(max_length=30)
    purchase_order = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)## quantity * purchase_cost

    def __str__(self):
        return f"{self.product.category.name} - {self.quantity} units"



# Sales System
class Sale(BaseModel):
    id = models.BigAutoField(primary_key=True)
    invoice = models.CharField(max_length=50) ## Auto Generate with combination current_date and month, product id, and categoryand brand
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale_date = models.DateField()
    gst = models.ForeignKey(GstMaster, on_delete=models.CASCADE)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2) #auto calculate
    total_amount = models.DecimalField(max_digits=15, decimal_places=2) #auto calculate

    def __str__(self):
        return f"Sale {self.customer.name} - {self.customer.contact_no}"


class SaleDetail(BaseModel):
    id = models.BigAutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_persentage = models.DecimalField(max_digits=10,decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2) ## auto calulate 
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.category.name} - {self.quantity} units"

# Transactions (Log Stock Movements)
class Transaction(BaseModel):
    id = models.BigAutoField(primary_key=True)
    TRANSACTION_TYPE_CHOICES = [
        ('Purchase', 'Purchase'),
        ('Sale', 'Sale'),
        ('Adjustment', 'Adjustment'),
    ]

    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()  # Negative for sales, positive for purchases
    reference_id = models.CharField(max_length=50, null=True, blank=True)  # Links to Purchase/Sale ID

    def __str__(self):
        return f"{self.transaction_type} - {self.product.sku} - {self.quantity}"

