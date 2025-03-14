from decimal import Decimal
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from inventory.forms import *
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist, ValidationError
# Create your views here.

def inv_index(request):
    return render(request,'master/index.html')


def footwear(request, action, ids=None):
    footwear_list = None
    form = FootwearForm()
    brand_form = BrandForm()
    footwearCategory_form = FootwearCategoryForm()
    material_form = MaterialForm()

    if action == "Save":
        if request.method == 'POST':
            if 'footwear' in request.POST:
                form = FootwearForm(request.POST)
                if form.is_valid():
                    brand = form.cleaned_data['brand']
                    category = form.cleaned_data['category']
                    low_stock_threshold = form.cleaned_data['low_stock_threshold']
                    description = form.cleaned_data['description']
                    category_ins = FootwearCategory.objects.get(id=category)
                    brand_ins = Brand.objects.get(id=brand)
                    if not Footwear.objects.filter( brand=brand_ins, category=category_ins).exists():
                        footwear_ins = Footwear.objects.create(
                            brand=brand_ins,
                            category=category_ins,
                            # materials=materials,
                            low_stock_threshold=low_stock_threshold,
                            description=description,
                        )
                        messages.success(request, "Data successfully created.")
                        return redirect('footwear', 'Save', None)
                    else:
                        messages.error(request, 'Data Already Exists.')
                else:
                    messages.error(request, 'Form Not Valid.')
            
            elif 'brand' in request.POST:
                brand_form = BrandForm(request.POST, request.FILES)
                if brand_form.is_valid():
                    name = brand_form.cleaned_data['name']
                    logo = brand_form.cleaned_data['logo']
                    description = brand_form.cleaned_data['description']

                    if not Brand.objects.filter(status=1, name=name).exists():
                        Brand.objects.create(name=name, logo=logo, description=description)
                        messages.success(request, 'Data Successfully Created.')
                        return redirect('footwear', 'Save', None)
                    else:
                        messages.error(request, 'Data Already Exists.')
                else:
                    messages.error(request, 'Form Not Valid.')

            elif 'footwearcategory' in request.POST:
                footwearCategory_form = FootwearCategoryForm(request.POST)
                if footwearCategory_form.is_valid():
                    name = footwearCategory_form.cleaned_data['name']
                    gender = footwearCategory_form.cleaned_data['gender']
                    description = footwearCategory_form.cleaned_data['description']

                    if not FootwearCategory.objects.filter(name=name, gender=gender, status=1).exists():
                        FootwearCategory.objects.create(name=name, gender=gender, description=description)
                        messages.success(request, 'Data Successfully Created.')
                        return redirect('footwear', 'Save', None)
                    else:
                        messages.error(request, 'Data Already Exists.')
                else:
                    messages.error(request, 'Form Not Valid.')

            

    elif action == 'Update' and ids:
        ids = int(ids)
        footwear_ins = get_object_or_404(Footwear, id=ids)
        initial_data = {
        'brand': footwear_ins.brand.id,
        'category': footwear_ins.category.id,
        'low_stock_threshold': footwear_ins.low_stock_threshold,
        'description': footwear_ins.description,
        }
        form = FootwearForm(initial=initial_data)
        if request.method == 'POST' and 'footwear' in request.POST:
            form = FootwearForm(request.POST)
            if form.is_valid():
                # name = form.cleaned_data['name']
                brand = form.cleaned_data['brand']
                category = form.cleaned_data['category']
                # materials = form.cleaned_data['materials']
                low_stock_threshold = form.cleaned_data['low_stock_threshold']
                description = form.cleaned_data['description']
                category_ins = FootwearCategory.objects.get(id=category)
                brand_ins = Brand.objects.get(id=brand)
                if not Footwear.objects.filter( brand=brand_ins, category=category_ins).exclude(id=ids).exists():
                    Footwear.objects.filter(id=ids).update(brand=brand_ins, category=category_ins,low_stock_threshold=low_stock_threshold ,description=description)
                    messages.success(request, 'Data Successfully Updated.')
                    return redirect('footwear', 'Save', None)
                else:
                    messages.error(request, 'Data Already Exists.')
            else:
                messages.error(request, 'Form Not Valid.')

    elif action == "Close" and ids:
        ids = int(ids)
        footwear_ins = get_object_or_404(Footwear, id=ids)
        initial_data = {
        'brand': footwear_ins.brand.id,
        'category': footwear_ins.category.id,
        'low_stock_threshold': footwear_ins.low_stock_threshold,
        'description': footwear_ins.description,
        }

        form = FootwearForm(initial=initial_data)
        for visible in form.visible_fields():
            visible.field.widget.attrs['disabled'] = True

        if request.method == 'POST':
            return redirect('footwear', 'List', None)
    elif action == "List":
        footwear_list = Footwear.objects.filter(status=1).order_by('-id')
        
        if request.method == 'POST':
            if 'DelData' in request.POST:
                DelData = request.POST['DelData']
                Footwear.objects.filter(id = DelData ).update(status = 0)
                messages.error(request,'Data Successfully Deactivate.')
            elif 'ActData' in request.POST:
                ActData = request.POST['ActData']
                Footwear.objects.filter(id = ActData ).update(status = 1)
                messages.success(request,'Data Successfully Activate.')
                      
    if action == 'List' :
        template = "master/footwear_list.html"
    else:
        template ='master/footwear.html'  
    context = {'action': action, 'form': form, 'brand_form': brand_form,  'material_form': material_form,
               'footwearCategory_form': footwearCategory_form,'footwear_list':footwear_list}
    return render(request, template, context)



def purchase(request, action, ids=None):
    purchase_list = None
    purchase_data = None
    footwear_variants = None
    form = PurchaseForm()
    gst_form = GstMasterForm()
    sup_form = SupplierForm()
    mat_form = MaterialForm()
    s_form = SizeForm()

    if action == "Save":
        if request.method == 'POST' and 'purchase' in request.POST:
            form = PurchaseForm(request.POST)
            try:
                supplier_id = request.POST.get('supplier')
                po_number = request.POST.get('po_number')
                po_date = request.POST.get('po_date')
                gst_id = request.POST.get('gst')
                gst_amount = request.POST.get('gst_amount', '0')
                total_amount = request.POST.get('total_amount', '0')
                active_status = request.POST.get('active_status', 'PEN')
                notes = request.POST.get('notes', '')

                if not supplier_id or not po_number or not po_date:
                    raise ValidationError("Supplier, PO number, and PO date are required.")

                if not total_amount.replace('.', '', 1).isdigit() or Decimal(total_amount) <= 0:
                    raise ValidationError("Total amount must be a positive number.")

                # Extract and validate FootwearVariant Details
                namelist = request.POST.getlist('name')
                footwearlist = request.POST.getlist('footwear')
                materialslist = request.POST.getlist('materials')
                sizelist = request.POST.getlist('size')
                quantitylist = request.POST.getlist('quantity')
                colorlist = request.POST.getlist('color')
                mrplist = request.POST.getlist('mrp')
                p_pricelist = request.POST.getlist('p_price')
                selling_pricelist = request.POST.getlist('selling_price')
                
                
                list_lengths = [len(namelist), len(footwearlist)]
                if len(set(list_lengths)) == 0:
                    raise ValidationError("All FootwearVariant details must have the same number of items.")

                supplier_ins = Supplier.objects.get(id=supplier_id)
                gst_ins = GstMaster.objects.get(id=gst_id) if gst_id else None

                try:
                    purchase_ins = Purchase.objects.create(
                        supplier=supplier_ins, 
                        gst=gst_ins,  
                        gst_amount=Decimal(gst_amount),
                        po_number=po_number,
                        po_date=datetime.datetime.strptime(po_date, '%d-%m-%Y'),
                        active_status=active_status,
                        total_amount=Decimal(total_amount),
                        notes=notes,
                    )
                except Exception as e:
                    print("Error creating purchase:", e)
                    raise
                # Prepare FootwearVariant instances for bulk creation
                variant_instances = []
                material_mappings = []
                for i in range(len(namelist)):
                    footwear_ins = Footwear.objects.get(id=footwearlist[i])
                    size_ins = Size.objects.get(id=sizelist[i])
                    materials_ins = Material.objects.get(id = materialslist[i])

                    footwear_variant = FootwearVariant(
                        footwear=footwear_ins,
                        purchase=purchase_ins,
                        material = materials_ins,
                        size=size_ins,
                        name=namelist[i],
                        color=colorlist[i],
                        quantity=int(quantitylist[i]),
                        p_price=Decimal(p_pricelist[i]),
                        selling_price=Decimal(selling_pricelist[i]),
                        mrp=Decimal(mrplist[i]),
                    )
                    variant_instances.append(footwear_variant)

                    # Store material IDs for later processing
                    material_ids = materialslist[i].split(',')
                    material_mappings.append(material_ids)
                # Bulk create FootwearVariant instances
                try:
                    created_variants = FootwearVariant.objects.bulk_create(variant_instances)
                    for variant in created_variants:
                        variant.stock_quantity += variant.quantity
                        variant.save(update_fields=['stock_quantity']) 
                except Exception as e:
                    print("Error creating Footwear Variant:", e)
                    raise
               

                messages.success(request, 'Data Successfully Created.')
                return redirect('purchase', 'List', None)

            except ObjectDoesNotExist as e:
                form.add_error(None, f"Related object not found: {str(e)}")
            except ValidationError as e:
                form.add_error(None, f"Validation error: {str(e)}")
            except Exception as e:
                form.add_error(None, f"Unexpected error: {str(e)}")
           
                
        elif request.method == 'POST' and 'supSave' in request.POST:
            sup_form = SupplierForm(request.POST)
            if sup_form.is_valid():
                name = request.POST.get('name')
                contact_person = request.POST.get('contact_person')
                contact_number = request.POST.get('contact_number')
                email = request.POST.get('email')
                address = request.POST.get('address')
                gst_number = request.POST.get('gst_number')
                payment_terms = request.POST.get('payment_terms')
                
                if not Supplier.objects.filter(contact_number = contact_number, status=1).exists():
                    Supplier.objects.create(
                        name = name,
                        contact_person= contact_person,
                        email =email,
                        address= address,
                        gst_number=gst_number,
                        payment_terms= payment_terms,
                    )
                    messages.success(request, 'Data Successfully Created.')
                    return redirect('purchase', 'Save', None)
                else:
                    messages.error(request, 'Data Already Exists.')
            else:
                messages.error(request, 'Form is Not Valid.')
        elif request.method == 'POST' and 'gstSave' in request.POST:
            gst_form = GstMasterForm(request.POST)
            if gst_form.is_valid():
                gst_type = request.POST.get('gst_type')
                gst_percentage = request.POST.get('gst_percentage')
                
                
                if not GstMaster.objects.filter(status=1,gst_type = gst_type,gst_percentage= gst_percentage ).exists():
                    GstMaster.objects.create(
                        gst_type = gst_type,
                        gst_percentage= gst_percentage,
                    )
                    messages.success(request, 'Data Successfully Created.')
                    return redirect('purchase', 'Save', None)
                else:
                    messages.error(request, 'Data Already Exists.')
            else:
                messages.error(request, 'Form is Not Valid.')
                
        elif request.method == 'POST' and 'sizeSave' in request.POST:
            s_form = SizeForm(request.POST)
            if s_form.is_valid():
                system = request.POST.get('system')
                value = request.POST.get('value')
                
                
                if not Size.objects.filter(status=1,system = system,value= value ).exists():
                    Size.objects.create(
                        system = system,
                        value= value,
                    )
                    messages.success(request, 'Data Successfully Created.')
                    return redirect('purchase', 'Save', None)
                else:
                    messages.error(request, 'Data Already Exists.')
            else:
                messages.error(request, 'Form is Not Valid.')
        
        elif request.method == 'POST' and 'footwearmaterial' in request.POST:
            material_form = MaterialForm(request.POST)
            if material_form.is_valid():
                name = material_form.cleaned_data['name']
                description = material_form.cleaned_data['description']

                if not Material.objects.filter(name=name, status=1).exists():
                    Material.objects.create(name=name, description=description)
                    messages.success(request, 'Data Successfully Created.')
                    return redirect('purchase', 'Save', None)
                else:
                    messages.error(request, 'Data Already Exists.')
            else:
                messages.error(request, 'Form is Not Valid.')
                
    elif action == "Close" and ids:
        ids = int(ids)
        purchase_list = Purchase.objects.select_related('gst', 'supplier' ).filter(id=ids).first()
        # purchase_list = Purchase.objects.select_related(
        #         'gst', 'supplier'
        #     ).filter(id=ids).only(
        #         'id', 'po_number', 'po_date', 'supplier__name', 'gst__gst_percentage', 
        #         'total_amount', 'notes'
        #     ).first()

            # Optimized Query for Related Data (Footwear Variants)
        # footwear_variants = FootwearVariant.objects.select_related(
        #     'footwear__category', 'footwear__brand', 'material', 'size'
        # ).filter(purchase_id=ids).only(
        #     'id', 'footwear__category__name', 'footwear__brand__name',
        #     'material__name', 'size__name', 'color', 'quantity', 'p_price'
        # )
        footwear_variants = FootwearVariant.objects.select_related('footwear__category', 'footwear__brand', 'material', 'size').filter(purchase_id=ids)
        
        
    elif action == "List":
        purchase_list = Purchase.objects.all().order_by('-id')
        
        if request.method == 'POST':
            if 'DelData' in request.POST:
                DelData = request.POST['DelData']
                Purchase.objects.filter(id = DelData ).update(status = 0)
                messages.error(request,'Data Successfully Deactivate.')
                return redirect('purchase', 'List', None)
            elif 'ActData' in request.POST:
                ActData = request.POST['ActData']
                Purchase.objects.filter(id = ActData ).update(status = 1)
                messages.success(request,'Data Successfully Activate.')
                return redirect('purchase', 'List', None)
    
    if action == 'List':
        template = 'master/purchase_list.html'
        
    elif action == 'Close':
        template = 'master/purchase_view.html'
        
    else:
        template = 'master/purchase.html'
    
    context= {'purchase_list':purchase_list,'form':form,'action':action,'gst_form':gst_form,
        'sup_form':sup_form,'mat_form':mat_form,'s_form':s_form,'footwear_variants':footwear_variants,'purchase_list':purchase_list }
    return render (request,template,context)


# def sale(request, action, ids=None):
#     curent_date = datetime.datetime.today()
#     footwear_variants = FootwearVariant.objects.select_related('footwear__category', 'footwear__brand', 'material').all().filter(status=1)
#     forms = CustomerForm()
#     sale_form = SaleForm()
#     if request.method == 'POST':
#         if action == "Save":
#             forms =CustomerForm(request.POST)
#             if forms.is_valid():
#                 pass
                
#         print(request.POST)
#     template = 'master/sale.html'
   
#     return render(request,template, context)


def sale(request, action, ids=None):
    current_date = datetime.datetime.today()
    footwear_variants = FootwearVariant.objects.filter(status=1,stock_quantity__gt=0).select_related('footwear__category', 'footwear__brand', 'material')
    forms = CustomerForm()
    sale_form = SaleForm()

    if action == "Save":
        if request.method == 'POST':
            forms = CustomerForm(request.POST)
            sale_form = SaleForm(request.POST)
            discount = request.POST['discount']
            total_amount = request.POST['total_amount']
            discount = request.POST['discount']
            discount = request.POST['discount']
            # Get or create the customer
            contact_number = request.POST['contact_number']
            customer_ins, created = Customer.objects.get_or_create(
                contact_number=contact_number, defaults={
                    'name': request.POST['name'],
                    'email': request.POST['email'],
                }
            )

            # Generate unique invoice number
            sale_id = Sale.objects.count() + 1
            invoice_number = f"AK/{current_date.strftime('%Y%m%d')}/{sale_id:06d}"
            gst = request.POST['gst']
            gst_ins = None
            if gst is not None:
                gst_ins = GstMaster.objects.get(id=gst)
        
                
            # Create Sale instance
            sale = Sale.objects.create(
                customer=customer_ins,
                invoice_number=invoice_number,
                sale_date=current_date.strftime("%Y-%m-%d"),
                payable_amount=request.POST['payable_amount'],
                discount=discount,
                gst=gst_ins,
                gst_amount=request.POST['gst_amount'],
                total_amount=total_amount,
                payment_method=request.POST['payment_method'],
                notes=request.POST['notes'],
            )

            # Process SaleDetail data from POST
            variant_ids = request.POST.getlist('footwear_variant')
            sizes = request.POST.getlist('footwear_size')
            quantities = request.POST.getlist('qty')
            selling_prices = request.POST.getlist('s_price')

            for i in range(len(variant_ids)):
                variant = get_object_or_404(FootwearVariant, id=variant_ids[i])
                size = get_object_or_404(Size, id=sizes[i])
                quantity = int(quantities[i])
                selling_price = Decimal(selling_prices[i])
            
                # Create SaleDetail entry
                SaleDetail.objects.create(
                    sale=sale,
                    variant=variant,
                    size=size,
                    quantity=quantity,
                    selling_price=selling_price,
                    sub_total_price=quantity * selling_price,
                )

                # Deduct stock quantity
                variant.stock_quantity -= quantity
                variant.save()

            messages.success(request, "Sale successfully created.")
            return redirect('sale', 'List', None)
        
    elif action == "List":
        sale_list = Sale.objects.all().order_by('-id')
        if request.method == 'POST':
            if 'DelData' in request.POST:
                DelData = request.POST['DelData']
                Sale.objects.filter(id = DelData ).update(status = 0)
                messages.error(request,'Data Successfully Deactivate.')
                return redirect('sale', 'List', None)
            elif 'ActData' in request.POST:
                ActData = request.POST['ActData']
                Sale.objects.filter(id = ActData ).update(status = 1)
                messages.success(request,'Data Successfully Activate.')
                return redirect('sale', 'List', None)
            
        template = "master/sale_list.html"
        context = {'sale_list': sale_list, 'action': action}
        return render(request, template, context)

    elif action == "Update" and ids:
        sale = get_object_or_404(Sale, id=ids)
        forms = CustomerForm(instance=sale.customer)
        sale_form = SaleForm(instance=sale)
        if request.method == 'POST':
            forms = CustomerForm(request.POST, instance=sale.customer)
            sale_form = SaleForm(request.POST, instance=sale)
            if forms.is_valid() and sale_form.is_valid():
                forms.save()
                sale_form.save()
                messages.success(request, "Sale successfully updated.")
                return redirect('sale', 'List', None)

    elif action == "Close" and ids:
        sale = (Sale.objects.select_related('customer', 'gst').prefetch_related('sale_details__variant', 'sale_details__size').get(id=ids))
        sale_details = sale.sale_details.all()
        template = "master/sale_view.html"
        context = {'sale': sale, 'sale_details': sale_details, 'action': action}
        return render(request, template, context)

    template = 'master/sale.html'
    context = { 'action': action,'ids': ids, 'forms': forms, 'sale_form': sale_form, 'current_date': current_date,  'footwear_variants': footwear_variants, }
    return render(request, template, context)
