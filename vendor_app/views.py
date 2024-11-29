import csv
from lib2to3.fixes.fix_input import context

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.views.generic import TemplateView
from xhtml2pdf import pisa
from django.db.models import Q
from Glenda_App.models import Menu
from customer_app.models import customer_registration
from register_app.forms import CustomUserForm, CustomLoginForm
from django.contrib import messages
from register_app.models import CustomUser, MenuPermissions
from vendor_app.forms import VendorRegisterForm, vendor_request_form
from vendor_app.models import vendor_register, vendor_request
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa




def vendor_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect after successful login
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = CustomLoginForm()

    return render(request,'front/vendor_login.html',{'form':form})



from django.urls import reverse

def front_logout(request):
    logout(request)
    # Redirect to a specific page after logout (e.g., home page)
    return redirect(reverse('customer_index'))

def signup(request):
    if request.method == 'POST':
        print("post")
        form = CustomUserForm(request.POST)
        if form.is_valid():
            lo = form.save(commit=False)
            lo.is_active=False
            print("valid")
            lo.save()
            messages.success(request, "Registration successful!")
            return redirect('login')
        messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserForm()

    return render(request,'front/sign_up.html',{'form':form})


@login_required(login_url='login')
def request(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    user=request.user
    if request.method == 'POST':
        print("post")
        form = vendor_request_form(request.POST,request.FILES)
        if form.is_valid():
            print("valid")
            vendor_request_instance = form.save(commit=False)  # Create instance without saving to database
            vendor_request_instance.user = user  # Set the user field
            vendor_request_instance.save()  # Now save with the user field included
            messages.success(request, "Request Send successfully!")
            return redirect('request')
        messages.error(request, "Please correct the errors below.")
    else:
        form = vendor_request_form()


    return render(request, "front/request.html",{'form':form,'allocated_menus':allocated_menus})

@login_required(login_url='login')
def my_profile(request):
    ven=request.user
    vendor=vendor_register.objects.get(user_id=ven.id)
    return render(request,'front/profile.html',{'vendor':vendor})

def vendor_request_list(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Define your custom order (e.g., by menu ID or another attribute)
    custom_order = ['Master', 'Purchase', 'Production', 'Inventory', 'Logistics', 'R & D', 'HR', 'Customer', 'Vendor',
                    'Accounts']  # replace with your actual menu IDs or names

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

    # Fetch all vendor_request objects
    vendor_requests = vendor_request.objects.filter(status='pending')
    context={
        'vendor_requests':vendor_requests,
        'allocated_menus':sorted_menus
    }

    # Render the template with the fetched data
    return render(request, 'front/vendor_request_list.html',context)

# def vendorlogin_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Redirect after successful login
#             else:
#                 form.add_error(None, "Invalid email or password")
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

def approve_as_vendor(request,id):
    ven = get_object_or_404(CustomUser,id=id)
    v=ven.id
    co =CustomUser.objects.get(id=v)
    co.is_active=True
    co.save()
    vendor =vendor_register()
    vendor.is_vendor=True
    vendor.user_id=v
    vendor.save()
    messages.success(request, "approved.")
    return redirect('view_customers_list')  # Redirect to the list view

def approve_as_distributor(request,id):
    ven = get_object_or_404(CustomUser,id=id)

    v=ven.id
    co = CustomUser.objects.get(id=v)
    co.is_active = True
    co.save()
    vendor =customer_registration()
    vendor.is_distributor=True
    vendor.user_id=v
    vendor.save()
    messages.success(request, "approved.")
    return redirect('view_customers_list')  # Redirect to the list view

def approve_as_customer(request,id):
    ven = get_object_or_404(CustomUser,id=id)
    ven.is_active=True
    ven.save()
    messages.success(request, "approved.")
    return redirect('view_vendor_list')  # Redirect to the list view


def vendor_verification(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Define your custom order (e.g., by menu ID or another attribute)
    custom_order = ['Master', 'Purchase', 'Production', 'Inventory', 'Logistics', 'R & D', 'HR', 'Customer', 'Vendor',
                    'Accounts']  # replace with your actual menu IDs or names

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
    vendor=vendor_register.objects.all()
    context={
        'vendor':vendor,
        'allocated_menus':sorted_allocated_menus

    }
    return render(request,'vendor/vendor_verification.html',context)

def approve_as_vendor_details(request,id):
    vendor = get_object_or_404(vendor_register,id=id)
    vendor.status="Approved"
    vendor.save()
    messages.success(request, "approved.")
    return redirect('vendor_verification')  # Redirect to the list view

















# vendor admin Page Details
def view_customers_list(request):
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

    view=CustomUser.objects.filter(is_staff=False,is_active=True)
    context = {
        'allocated_menus': sorted_allocated_menus,
        'view':view

    }
    return render(request,'customer/Reg_customers.html',context)


def view_vendors(request):
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
    view = vendor_register.objects.filter(status='pending')
    return render(request,'vendor/view_vendors.html',{'view':view,'allocated_menus':sorted_allocated_menus})




def view_vendor_profile(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    view = vendor_register.objects.get(user_id=id)

    return render(request,'vendor/view_vendor_profile.html',{'view':view,'menus':menus,'id':id})


def vender_register_view(request):
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


    # Fetching menus and their related submenus for display
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.is_active = True  # Set the user as inactive initially
            vendor.save()

            # If you have many-to-many fields, save them explicitly
            form.save_m2m()

            messages.success(request, "Registration successful!")
            return redirect('view_vendor_list')  # Adjust the URL pattern name as needed
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserForm()

    # Assuming menus need to be fetched from a model, add your logic to get them
    # menus = Menu.objects.all()  # Example, replace with actual query
    return render(request, 'vendor/vendor_reg.html', {'form': form,'allocated_menus':sorted_allocated_menus})


def vendor_details(request, vendor_id):
    try:
        # Retrieve the vendor object by its ID
        vendor = vendor_register.objects.get(id=vendor_id)

        # Prepare the data to be returned as JSON
        vendor_data = {
            'name': vendor.user.name,
            'company_name': vendor.company_name,
            'materials': [material.name for material in vendor.materials_name.all()],
            'vendor_district': vendor.vendor_district,
            'vendor_state': vendor.vendor_state,
            'vendor_country': vendor.vendor_country,
            'vendor_pincode': vendor.vendor_pincode,
            'vendor_Street': vendor.vendor_Street,
            'vendor_Landmark': vendor.vendor_Landmark,
            'vendor_Building': vendor.vendor_Building,
            'vendor_PANNBR': vendor.vendor_PANNBR if vendor.pan_yes_or_no == 'yes' else 'Not Provided',
        }

        # Return the data as JSON
        return JsonResponse(vendor_data)

    except vendor_register.DoesNotExist:
        # If the vendor is not found, return a not found message
        return JsonResponse({'error': 'Vendor not found'}, status=404)


def create_vendor_details(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()
    mem = get_object_or_404(vendor_register,user_id=id)


    if request.method == 'POST':
        form = VendorRegisterForm(request.POST, request.FILES,instance=mem)  # Added request.FILES for file uploads if needed
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user_id = id
            vendor.status='pending'
            # Associate the user
            vendor.save()
            form.save_m2m()  # Save the many-to-many field for materials
            return redirect('view_vendors')  # Redirect to vendor list after successful submission
    else:
        form = VendorRegisterForm()

    return render(request, 'vendor/add_vendor_details.html', {'form': form, 'menus': menus})

def edit_vender(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    us = CustomUser.objects.get(id=id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST,request.FILES,instance=us)
        if form.is_valid():
            form.save()
            messages.success(request, "Vendor updated successfully!")
            return redirect('view_vendor_list')  # Redirect to a relevant page (e.g., user list or dashboard)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserForm(instance=us)
    return render(request, 'vendor/update_vender.html', {'form': form,'menus':menus})

def delete_vender_view(request, user_id):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Retrieve the user object to be deleted
    us = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        # If confirmed, delete the user
        us.delete()
        messages.success(request, "Vender deleted successfully!")
        return redirect('view_vendor_list')  # Redirect to a list of users or homepage

    # If request is GET, prompt confirmation
    return render(request, 'Vendor/delete_vendor.html', {'us': us,'menus':menus})



def vendor_details_pdf(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()
    view = vendor_register.objects.filter(user_id=id).first()

    context = {'view': view, 'menu': menus}
    template = get_template('vendor/vendor_details_pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vendor_profile_{view.user.name}.pdf"'

    pdf_status = pisa.CreatePDF(
        html,
        dest=response
    )
    return response


def vendor_list_csv(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    view = CustomUser.objects.filter(is_staff=False)

    context = {'view': view, 'menu': menus}
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = f'attachment; filename="vendor_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone Number'])

    vendors = CustomUser.objects.filter(is_staff=False)

    for vendor in vendors:
        writer.writerow([vendor.name, vendor.email, vendor.phone_number])

    return response



def vendor_search_and_export(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    vendor_list = CustomUser.objects.filter(is_staff=False)  # Default to all vendors

    filters = Q()  # Initialize filters as an empty Q object

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '').strip()
        export_format = request.GET.get('export', '')

        if search_query:
            # Build filters based on the search query
            if search_query.isdigit():
                filters &= Q(phone_number__icontains=search_query, is_staff=False)  # Filter by phone number
            else:
                filters &= Q(name__icontains=search_query, is_staff=False)  # Filter by name

        # Apply filters if any were provided
        if filters:
            vendor_list = CustomUser.objects.filter(filters)

        if export_format == 'csv':
            # CSV export
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="vendor_list.csv"'

            writer = csv.writer(response)
            writer.writerow(['Name', 'Email', 'Phone Number'])

            for vendor in vendor_list:
                writer.writerow([vendor.name, vendor.email, vendor.phone_number])

            return response

    context = {
        'view': vendor_list,  # This will be used in the template
        'menus': menus,
    }

    return render(request, 'vendor/Reg_customers.html', context)

