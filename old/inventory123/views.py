from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum, Count, F, Q
from django.db import transaction
from .serializers import *
from .models import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender']
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = Footwear.objects.filter(category=category)
        serializer = FootwearSerializer(products, many=True)
        return Response(serializer.data)

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        brand = self.get_object()
        products = Footwear.objects.filter(brand=brand)
        serializer = FootwearSerializer(products, many=True)
        return Response(serializer.data)

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['season', 'year']
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def current_season(self, request):
        today = timezone.now().date()
        current_year = today.year
        month = today.month
        
        season_mapping = {
            (3, 4, 5): 'SPR',
            (6, 7, 8): 'SUM',
            (9, 10, 11): 'FAL',
            (12, 1, 2): 'WIN'
        }
        
        current_season = next(
            season for months, season in season_mapping.items() 
            if month in months
        )
        
        collection = self.queryset.filter(
            year=current_year,
            season=current_season
        )
        serializer = self.get_serializer(collection, many=True)
        return Response(serializer.data)

class FootwearViewSet(viewsets.ModelViewSet):
    queryset = Footwear.objects.all()
    serializer_class = FootwearSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand', 'collection', 'is_active']
    search_fields = ['name', 'style_code']

    @action(detail=True, methods=['get'])
    def low_stock_variants(self, request, pk=None):
        footwear = self.get_object()
        variants = footwear.variants.filter(
            stock_quantity__lte=F('footwear__low_stock_threshold')
        )
        serializer = FootwearVariantSerializer(variants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def sales_analytics(self, request, pk=None):
        footwear = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        sales_query = SaleDetail.objects.filter(
            variant__footwear=footwear
        )
        
        if start_date:
            sales_query = sales_query.filter(sale__sale_date__gte=start_date)
        if end_date:
            sales_query = sales_query.filter(sale__sale_date__lte=end_date)
            
        analytics = sales_query.aggregate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('selling_price')),
            total_sales=Count('sale', distinct=True)
        )
        
        return Response(analytics)

class FootwearVariantViewSet(viewsets.ModelViewSet):
    queryset = FootwearVariant.objects.all()
    serializer_class = FootwearVariantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['footwear', 'color', 'size']
    search_fields = ['sku', 'barcode']

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        variant = self.get_object()
        quantity = request.data.get('quantity', 0)
        reason = request.data.get('reason', '')
        
        if not reason:
            raise ValidationError({'reason': 'Reason is required for stock adjustment'})
            
        variant.stock_quantity += quantity
        if variant.stock_quantity < 0:
            raise ValidationError({'quantity': 'Stock cannot be negative'})
            
        variant.save()
        
        # Create stock adjustment record
        StockAdjustment.objects.create(
            product=variant.footwear,
            adjustment_reason=reason,
            adjusted_quantity=quantity
        )
        
        return Response({
            'message': 'Stock adjusted successfully',
            'new_stock': variant.stock_quantity
        })

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'contact_person', 'contact_number', 'email', 'gst_number']

    @action(detail=True, methods=['get'])
    def purchase_history(self, request, pk=None):
        supplier = self.get_object()
        purchases = Purchase.objects.filter(supplier=supplier)
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def pending_payments(self, request, pk=None):
        supplier = self.get_object()
        pending_purchases = Purchase.objects.filter(
            supplier=supplier,
            status__in=['PEN', 'PAR']
        )
        total_pending = pending_purchases.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        return Response({
            'pending_amount': total_pending,
            'pending_purchases': PurchaseSerializer(pending_purchases, many=True).data
        })

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['supplier', 'status', 'po_date']
    search_fields = ['po_number']

    @action(detail=True, methods=['post'])
    def receive_items(self, request, pk=None):
        purchase = self.get_object()
        details = request.data.get('details', [])
        
        with transaction.atomic():
            for detail in details:
                purchase_detail = PurchaseDetail.objects.get(
                    id=detail['id'], purchase=purchase
                )
                received_qty = detail.get('received_quantity', 0)
                if received_qty > 0:
                    purchase_detail.received_quantity = received_qty
                    purchase_detail.save()
            
            # Update purchase status
            total_items = purchase.details.count()
            received_items = purchase.details.filter(
                received_quantity__gt=0
            ).count()
            
            if received_items == 0:
                purchase.status = 'PEN'
            elif received_items == total_items:
                purchase.status = 'REC'
            else:
                purchase.status = 'PAR'
            
            purchase.save()
            
        return Response({'status': 'success'})

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'contact_number', 'email']

    @action(detail=True, methods=['get'])
    def purchase_history(self, request, pk=None):
        customer = self.get_object()
        sales = Sale.objects.filter(customer=customer).order_by('-sale_date')
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def redeem_points(self, request, pk=None):
        customer = self.get_object()
        points_to_redeem = int(request.data.get('points', 0))
        
        if points_to_redeem > customer.loyalty_points:
            raise ValidationError('Insufficient loyalty points')
        
        customer.loyalty_points -= points_to_redeem
        customer.save()
        
        return Response({
            'message': f'{points_to_redeem} points redeemed successfully',
            'remaining_points': customer.loyalty_points
        })

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['customer', 'sale_date', 'payment_method']
    search_fields = ['invoice_number']

    def create(self, request, *args, **kwargs):
        data = request.data
        details = data.pop('details', [])
        
        with transaction.atomic():
            # Calculate totals
            subtotal = sum(
                detail['quantity'] * detail['selling_price'] 
                for detail in details
            )
            discount = data.get('discount', 0)
            tax = subtotal * 0.18  # Assuming 18% GST
            total_amount = subtotal - discount + tax
            
            # Create sale
            data.update({
                'subtotal': subtotal,
                'tax': tax,
                'total_amount': total_amount
            })
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            sale = serializer.save()
            
            # Create sale details
            for detail in details:
                detail['sale'] = sale.id
                detail_serializer = SaleDetailSerializer(data=detail)
                detail_serializer.is_valid(raise_exception=True)
                detail_serializer.save()
            
            # Update customer loyalty points
            if sale.customer:
                points_earned = int(total_amount / 100)  # 1 point per 100 currency
                sale.customer.loyalty_points += points_earned
                sale.customer.save()
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        date = request.query_params.get('date', timezone.now().date())
        
        sales = Sale.objects.filter(sale_date=date)
        summary = {
            'total_sales': sales.count(),
            'total_amount': sales.aggregate(total=Sum('total_amount'))['total'] or 0,
            'payment_methods': sales.values('payment_method').annotate(
                count=Count('id'),
                total=Sum('total_amount')
            )
        }
        
        return Response(summary)

class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['return_type', 'status', 'return_date']
    search_fields = ['sale__invoice_number']

    def create(self, request, *args, **kwargs):
        data = request.data
        
        # Validate return period
        sale = Sale.objects.get(id=data['sale'])
        if (timezone.now().date() - sale.sale_date).days > 30:
            raise ValidationError('Returns are only allowed within 30 days of purchase')
        
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def process_return(self, request, pk=None):
        return_obj = self.get_object()
        action = request.data.get('action')
        
        if action not in ['approve', 'reject']:
            raise ValidationError('Invalid action')
            
        if return_obj.status != 'PEN':
            raise ValidationError('Return is not in pending status')
            
        if action == 'approve':
            return_obj.status = 'APR'
        else:
            return_obj.status = 'REJ'
            
        return_obj.save()
        return Response({'status': 'success'})

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def active(self, request):
        today = timezone.now().date()
        promotions = self.queryset.filter(
            start_date__lte=today,
            end_date__gte=today,
            is_active=True
        )
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def applicable_products(self, request, pk=None):
        promotion = self.get_object()
        products = Footwear.objects.filter(
            Q(category__in=promotion.applicable_categories.all()) |
            Q(brand__in=promotion.applicable_brands.all())
        ).distinct()
        serializer = FootwearSerializer(products, many=True)
        return Response(serializer.data)

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'date']
    search_fields = ['description']

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        year = request.query_params.get('year', timezone.now().year)
        month = request.query_params.get('month', timezone.now().month)
        
        expenses = self.queryset.filter(
            date__year=year,
            date__month=month
        )
        
        summary = expenses.values('category__name').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        )
        
        total = expenses.aggregate(
            total_amount=Sum('amount'),
            total_count=Count('id')
        )
        
        return Response({
            'summary': summary,
            'total': total,
            'year': year,
            'month': month
        })