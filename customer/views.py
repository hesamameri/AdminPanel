from django.shortcuts import render
from django.db.models import F
from .models import CustomerSubSVA
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

def customer_index(request):
    distinct_obj_item_ids = CustomerSubSVA.objects.values('obj_item_id').distinct()

    # Initialize an empty dictionary to store the merged records
    merged_records = {}

    # Loop through the distinct obj_item_ids
    for item in distinct_obj_item_ids:
        obj_item_id = item['obj_item_id']

        # Check if the obj_item_id already exists in the merged_records dictionary
        if obj_item_id not in merged_records:
            # If not, initialize a dictionary for the obj_item_id
            merged_records[obj_item_id] = {
                'obj_item_id': obj_item_id,
                'name': None,
                'title': None,
                'status': None,
                'city_id': None,
                'codemeli': None,
                'mobile': None,
                'title': None,
                'phone':None,
                'reagent':None,
                'address':None,
                # Add other fields as needed
            }

        # Get the CustomerSubSVA objects for the current obj_item_id
        customer_records = CustomerSubSVA.objects.filter(obj_item_id=obj_item_id)

        # Loop through the records and update the merged record with non-null fields
        for record in customer_records:
            if record.name:
                merged_records[obj_item_id]['name'] = record.name
            if record.title:
                merged_records[obj_item_id]['title'] = record.title
            if record.status:
                merged_records[obj_item_id]['status'] = record.status
            if record.city_id:
                merged_records[obj_item_id]['city_id'] = record.city_id
            if record.codemeli:
                merged_records[obj_item_id]['codemeli'] = record.codemeli
            if record.mobile:
                merged_records[obj_item_id]['mobile'] = record.mobile
            # Add other fields as needed

    # Convert the dictionary values to a list to use for pagination
    merged_records_list = list(merged_records.values())

    # Set the number of records to display per page
    records_per_page = 15

    # Initialize the Paginator object with the data and the number of records per page
    paginator = Paginator(merged_records_list, records_per_page)

    # Get the current page number from the request's GET parameters. If not provided, default to 1.
    page_number = request.GET.get('page', 1)

    try:
        # Get the Page object for the requested page number
        page = paginator.page(page_number)
    except EmptyPage:
        # If the requested page number is out of range, display the last page
        page = paginator.page(paginator.num_pages)

    context = {
        'page': page,
    }

    return render(request, 'Customer/CustomerIndex.html', context=context)
