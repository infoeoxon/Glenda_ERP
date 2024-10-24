
from django.shortcuts import render, redirect, get_object_or_404

from Glenda_App.models import Menu
from purchase_app.forms import CategoryForm, RawMaterialForm

from django.contrib import messages
from django.db.models import Q

from purchase_app.models import RawMaterials, RawMaterialCategory
from register_app.models import MenuPermissions
from inventory_app.models import Raw_material_request


# Create your views here.


def view_rawmaterials(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    view_ca=RawMaterialCategory.objects.all()
    view=RawMaterials.objects.all()
    categories = RawMaterialCategory.objects.all()
    return render(request,'purchase/view_rawmaterials.html',{'view':view,'view_ca':view_ca,'menus':menus, 'categories': categories})

def add_category(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print("Request")
        if form.is_valid():
            print("Success")
            form.save()
            messages.success(request, 'Successfull')

            return redirect('view_rawmaterials')
    return render(request, 'purchase/Add_category.html', {'form': form, 'menus': menus})


def create_raw_material(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    if request.method == 'POST':
        form = RawMaterialForm(request.POST, request.FILES)  # Use request.FILES for file upload
        if form.is_valid():
            form.save()
            return redirect('view_rawmaterials')  # Redirect to a list view or another page after saving
    else:
        form = RawMaterialForm()

    return render(request, 'purchase/add_rawmaterials.html', {'form': form, 'menus': menus})

def update_rawmaterials(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()

    mem = get_object_or_404(RawMaterials, id=id)

    if request.method == 'POST':
        form = RawMaterialForm(request.POST, instance=mem)
        if form.is_valid():
            form.save()
            return redirect('view_rawmaterials')  # Redirect to the list view or any relevant view
    else:
        form = RawMaterialForm(instance=mem)

    return render(request, 'purchase/update_rawmaterials.html', {'form': form, 'menus': menus})


def delete_rawmaterils(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Fetch the object or return a 404 error if not found
    dtl = get_object_or_404(RawMaterials, id=id)

    if request.method == "POST":
        dtl.delete()
        return redirect('view_rawmaterials')

    # Render the confirmation page for GET requests
    return render(request, 'purchase/delete_rawmaterials.html', {'dtl': dtl,'menus':menus})


def message_request(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    message = Raw_material_request.objects.all()

    return render(request,'purchase/message_request_list.html', {'menus': menus, 'message':message})


def message_response(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Fetch the specific request by its primary key (id)
    request_data = get_object_or_404(Raw_material_request, pk=id)

    if request.method == 'POST':

        print(request.POST)  # Debugging: Print the POST data

        if 'accept' in request.POST:
            # If 'Accept' button is clicked, set status to 'completed'
            request_data.status = 'Completed'
            request_data.save()
            return redirect('message_requests')

        elif 'decline' in request.POST:
            decline_reason = request.POST.get('response')

            if decline_reason:
                request_data.status = 'Declined'
                request_data.response = decline_reason  # Save decline reason
                request_data.save()
                return redirect('message_requests')
            else:
                error_message = "Please provide a reason for declining"

                return render(request, 'purchase/message_request_view.html', {
                    'data': request_data,
                    'menus': menus,
                    'error_message': error_message})

    return render(request, 'purchase/message_request_view.html', {
        'data': request_data,
        'menus': menus
    })


def raw_material_purchase_search(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    categories = RawMaterialCategory.objects.all()  # Get distinct categories
    raw_materials = RawMaterials.objects.prefetch_related('stocks').all()

    context = {
        'view': raw_materials,
        'categories': categories,
        'menus': menus
    }

    if request.method == 'POST':
        category = request.POST.get('category', None)  # Get category from form
        name = request.POST.get('name', None)          # Get name from form

        filters = Q()

        # Apply category filter if selected
        if category and category.isdigit():
            filters &= Q(category_id=int(category))

        # Apply name filter if provided
        if name:
            filters &= Q(name__icontains=name)

        # Filter stock based on combined filters
        if filters:
            search_list = RawMaterials.objects.filter(filters)

            # Debugging: Logging or print statement
            print(f"Filters applied: {filters}")
            print(f"Filtered records count: {search_list.count()}")

    context['view'] = search_list # Filtered stock data

    return render(request, 'purchase/view_rawmaterials.html', context)

