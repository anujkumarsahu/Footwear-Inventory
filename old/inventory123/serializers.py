from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class FootwearImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootwearImage
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class FootwearVariantSerializer(serializers.ModelSerializer):
    size_details = SizeSerializer(source='size', read_only=True)
    
    class Meta:
        model = FootwearVariant
        fields = '__all__'

class FootwearSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    brand_details = BrandSerializer(source='brand', read_only=True)
    collection_details = CollectionSerializer(source='collection', read_only=True)
    materials_details = MaterialSerializer(many=True, source='materials', read_only=True)
    images = FootwearImageSerializer(many=True, read_only=True)
    variants = FootwearVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Footwear
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseDetailSerializer(serializers.ModelSerializer):
    variant_details = FootwearVariantSerializer(source='variant', read_only=True)
    
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    details = PurchaseDetailSerializer(many=True, read_only=True)
    supplier_details = SupplierSerializer(source='supplier', read_only=True)
    
    class Meta:
        model = Purchase
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class SaleDetailSerializer(serializers.ModelSerializer):
    variant_details = FootwearVariantSerializer(source='variant', read_only=True)
    
    class Meta:
        model = SaleDetail
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True, read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'

class ReturnSerializer(serializers.ModelSerializer):
    sale_details = SaleSerializer(source='sale', read_only=True)
    variant_details = FootwearVariantSerializer(source='variant', read_only=True)
    
    class Meta:
        model = Return
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    applicable_categories_details = CategorySerializer(many=True, source='applicable_categories', read_only=True)
    applicable_brands_details = BrandSerializer(many=True, source='applicable_brands', read_only=True)
    
    class Meta:
        model = Promotion
        fields = '__all__'

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    category_details = ExpenseCategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'