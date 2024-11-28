from django.shortcuts import render, redirect

# Create your views here.
import csv
from lib2to3.pgen2.driver import Driver
from django.http import HttpResponse, JsonResponse

from customer_app.forms import RegistrationForm
from customer_app.models import customer_registration
from register_app.models import MenuPermissions


def view_dealers(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Define your custom order (e.g., by menu ID or another attribute)
    custom_order = ['Master', 'Purchase', 'Production','Inventory','Logistics','R & D','HR','Customer','Vendor','Accounts']  # replace with your actual menu IDs or names

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    # Sort menus based on custom order
    sorted_menus = sorted(
        allocated_menus.items(),
        key=lambda x: custom_order.index(x[0].title) if x[0].title in custom_order else float('inf')
    )

    # Create a new dictionary for sorted menus
    sorted_allocated_menus = dict(sorted_menus)
    view = customer_registration.objects.all()
    return render(request,'customer/dealers_list.html',{'view':view,'allocated_menus':sorted_allocated_menus})

def create_customer_details(request,id):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Define your custom order (e.g., by menu ID or another attribute)
    custom_order = ['Master', 'Purchase', 'Production','Inventory','Logistics','R & D','HR','Customer','Vendor','Accounts']  # replace with your actual menu IDs or names

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    # Sort menus based on custom order
    sorted_menus = sorted(
        allocated_menus.items(),
        key=lambda x: custom_order.index(x[0].title) if x[0].title in custom_order else float('inf')
    )

    # Create a new dictionary for sorted menus
    sorted_allocated_menus = dict(sorted_menus)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)  # Added request.FILES for file uploads if needed
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user_id = id  # Associate the user
            vendor.save()
            form.save_m2m()  # Save the many-to-many field for materials
            return redirect('view_dealers')  # Redirect to vendor list after successful submission
    else:
        form = RegistrationForm()

    return render(request, 'customer/registration.html', {'form': form, 'allocated_menus': sorted_allocated_menus})



def get_customer_details(request, customer_id):
    try:
        customer = customer_registration.objects.get(id=customer_id)
        customer_data = {
            'name': customer.user.name,
            'address': customer.address,
            'pincode': customer.pincode,
            'state': customer.state,
            'district': customer.district,
            'email': customer.email,
            'GST_yes_or_no': customer.GST_yes_or_no,
            'GST_number': customer.GST_number,
            'PAN_yes_or_no': customer.pan_yes_or_no,
            'PAN_number': customer.PAN_number,
            'phone_number': customer.phone_number
        }
        return JsonResponse(customer_data)
    except customer_registration.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

def contact(request):
    return render(request,'front/contact.html')


def about(request):
    return render(request,'front/about.html')

def Certificate(request):
    return render(request,'front/certificate.html')

def quality(request):
    return render(request,'front/quality.html')


def Steps(request):
    return render(request,'front/steps.html')




















def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_customeruser')  # Redirect to a success page or another appropriate page
    else:
        form = RegistrationForm()

    return render(request, 'customer/registration.html', {'form': form, 'menus': menus})


def view_customeruser(request):
    view = customer_registration.objects.all()
    return render(request, 'customer/viewcustomer.html', {'menus': menus, 'view': view})


def customer_search(request):
    customer_list = customer_registration.objects.all()  # Default to all vendors

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '').strip()

        if search_query:
            # Build filters
            filters = Q()

        if search_query.isdigit():
            filters &= Q(phone_number__icontains=search_query)  # Filter by user name

        else:
            filters &= Q(name__icontains=search_query)  # Filter by vendor phone number

        # Apply filters if any were provided
    if filters:
        customer_list = customer_registration.objects.filter(filters)

    context = {
        'view': customer_list,  # This will be used in the template
    }

    return render(request, 'customer/viewcustomer.html', context)


def view_customer_profile(request, id):

    view = customer_registration.objects.filter(user_id=id)

    return render(request, 'customer/search_profile.html', {'view': view, 'menus': menus})


def customer_list_csv(request):
    view = customer_registration.objects.all()

    context = {'view': view, }
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = f'attachment; filename="customer_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone Number'])

    customers = customer_registration.objects.all()

    for customer in customers:
        writer.writerow([customer.name, customer.phone_number])

    return response


def customer_exportsearch(request):
    # Prefetch menus for rendering in the template
    export_format = request.GET.get('export', '')
    search_query = request.GET.get('search_query', '').strip()  # Search by name or phone number

    # Initialize the filters
    filters = Q()

    # Initialize the export list based on the search query
    if search_query:
        # Check if the search query is a digit (indicating a phone number)
        if search_query.isdigit():
            filters &= Q(phone_number__icontains=search_query)
        else:
            filters &= Q(name__icontains=search_query)

    # Fetch the filtered list based on the constructed filters
    searchexport_list = customer_registration.objects.filter(filters)

    # If 'export' parameter is found, handle CSV export
    if export_format == 'excel':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Customer_searchexport_List.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['Name', 'Address', 'State', 'District', 'Pincode', 'Email', 'GST Number', 'PAN Number', 'Phone Number'])

        for customer in searchexport_list:
            writer.writerow([
                customer.name,
                customer.address,
                customer.state,
                customer.district,
                customer.pincode,
                customer.email,
                customer.GST_number,
                customer.PAN_number,
                customer.phone_number
            ])

        return response  # Return CSV response for download

    # Prepare the context to render in the template
    context = {
        'view': searchexport_list,  # Filtered customer list for display
           # Menus for navigation
        'search_query': search_query,  # Keep search query in the context for display in form
    }

    # Render the combined view template
    return render(request, 'customer/viewcustomer.html', context)