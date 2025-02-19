from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'footwear', FootwearViewSet)
router.register(r'variants', FootwearVariantViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'returns', ReturnViewSet)
router.register(r'promotions', PromotionViewSet)
router.register(r'expense-categories', ExpenseCategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]