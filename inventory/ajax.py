from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from inventory.models import *

# @csrf_exempt
def get_gst_percentage(request):
    if request.method == 'POST':
        gst_type = request.POST.get('gst')
        if gst_type:
            try:
                gst = GstMaster.objects.get(id=gst_type)
                return JsonResponse({'gst_percentage': float(gst.gst_percentage)})
            except GstMaster.DoesNotExist:
                return JsonResponse({'error': 'GST type not found'}, status=404)
        return JsonResponse({'error': 'Invalid GST type'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_footwear_sizes(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        amount_mrp = 0
        try:
            variant = FootwearVariant.objects.get(id=variant_id)
            size_ids = FootwearVariant.objects.filter(footwear=variant.footwear,status=1).values_list('size_id', flat=True)
            # system = variant.size.system
            amount_mrp = variant.mrp
            if size_ids:
                sizes = Size.objects.filter(id__in=size_ids)
            else:
                 sizes = Size.objects.all().filter(status=1)
            size_data = [{"id": size.id, "value": f"{size.system} - {size.value}"} for size in sizes]
            return JsonResponse({'sizes': size_data,'amount_mrp':amount_mrp})
        except FootwearVariant.DoesNotExist:
            return JsonResponse({'error': 'Variant not found'}, status=404)

def get_categories(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id')
    # Filter categories linked to the selected brand via Footwear
        category_ids = Footwear.objects.filter(brand_id=brand_id).values_list('category_id', flat=True).distinct()
        categories = FootwearCategory.objects.filter(id__in=category_ids).values('id', 'name', 'gender').order_by('name')

        category_list = [{'id': cat['id'], 'name': f"{cat['name']} - {cat['gender']}"} for cat in categories]
    
        return JsonResponse({'categories': category_list})
    else:
        return JsonResponse({'error': 'Categories not found'}, status=404)