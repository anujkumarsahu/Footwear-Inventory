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
            system = variant.size.system
            amount_mrp = variant.mrp
            sizes = Size.objects.filter(system=system)
            size_data = [{"id": size.id, "value": f"{size.system} - {size.value}"} for size in sizes]
            return JsonResponse({'sizes': size_data,'amount_mrp':amount_mrp})
        except FootwearVariant.DoesNotExist:
            return JsonResponse({'error': 'Variant not found'}, status=404)