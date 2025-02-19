from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_logo', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "No Logo"
    display_logo.short_description = 'Logo'

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'year', 'created_at')
    list_filter = ('season', 'year')
    search_fields = ('name',)
    ordering = ('-year', 'season', 'name')

class FootwearImageInline(admin.TabularInline):
    model = FootwearImage
    extra = 1

class FootwearVariantInline(admin.TabularInline):
    model = FootwearVariant
    extra = 1
    autocomplete_fields = ['size']

@admin.register(Footwear)
class FootwearAdmin(admin.ModelAdmin):
    list_display = ('name', 'style_code', 'brand', 'category', 'mrp', 'is_active')
    list_filter = ('brand', 'category', 'collection', 'is_active', 'created_at')
    search_fields = ('name', 'style_code')
    autocomplete_fields = ['brand', 'category', 'collection', 'materials']
    inlines = [FootwearImageInline, FootwearVariantInline]
    filter_horizontal = ('materials',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'style_code', 'brand', 'category', 'collection')
        }),
        ('Details', {
            'fields': ('description', 'features', 'care_instructions', 'materials')
        }),
        ('Pricing & Stock', {
            'fields': ('mrp', 'low_stock_threshold', 'is_active')
        }),
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('system', 'value')
    list_filter = ('system',)
    search_fields = ('value',)
    ordering = ('system', 'value')

@admin.register(FootwearVariant)
class FootwearVariantAdmin(admin.ModelAdmin):
    list_display = ('footwear', 'color', 'size', 'sku', 'stock_quantity', 'selling_price')
    list_filter = ('footwear__brand', 'footwear__category')
    search_fields = ('sku', 'barcode', 'footwear__name')
    autocomplete_fields = ['footwear', 'size']
    list_editable = ('stock_quantity', 'selling_price')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_number', 'email', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'contact_person', 'contact_number', 'email', 'gst_number')

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1
    autocomplete_fields = ['variant']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'supplier', 'po_date', 'expected_delivery', 'status', 'total_amount')
    list_filter = ('status', 'po_date', 'expected_delivery')
    search_fields = ('po_number', 'supplier__name')
    autocomplete_fields = ['supplier']
    inlines = [PurchaseDetailInline]
    date_hierarchy = 'po_date'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'email', 'loyalty_points', 'created_at')
    search_fields = ('name', 'contact_number', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 1
    autocomplete_fields = ['variant']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'sale_date', 'total_amount', 'payment_method')
    list_filter = ('payment_method', 'sale_date')
    search_fields = ('invoice_number', 'customer__name')
    autocomplete_fields = ['customer']
    inlines = [SaleDetailInline]
    date_hierarchy = 'sale_date'

    readonly_fields = ('subtotal', 'total_amount')

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('sale', 'variant', 'quantity', 'return_date', 'return_type', 'status')
    list_filter = ('return_type', 'status', 'return_date')
    search_fields = ('sale__invoice_number', 'variant__sku')
    autocomplete_fields = ['sale', 'variant']
    date_hierarchy = 'return_date'

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'discount_percentage', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name',)
    filter_horizontal = ('applicable_categories', 'applicable_brands')
    date_hierarchy = 'start_date'

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'date', 'amount', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'
    autocomplete_fields = ['category']

# Customize admin site header and title
admin.site.site_header = 'Footwear Shop Administration'
admin.site.site_title = 'Footwear Shop Admin'
admin.site.index_title = 'Footwear Shop Management'