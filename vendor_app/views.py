import csv

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
from Glenda_App.models import Menu
from register_app.forms import CustomUserForm
from django.contrib import messages
from register_app.models import CustomUser
from vendor_app.forms import VendorRegisterForm
from vendor_app.models import vendor_register

from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa


# Create your views here.

def view_vendor_list(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    view=CustomUser.objects.filter(is_staff=False)
    for user in view:
        user.details_added = vendor_register.objects.filter(user=user).exists()


    return render(request,'vendor/view_vendor_list.html',{'view':view,'menus':menus})

def view_vendor_profile(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    view = vendor_register.objects.get(user_id=id)

    return render(request,'vendor/view_vendor_profile.html',{'view':view,'menus':menus,'id':id})

def vender_register_view(request):
    # Fetching menus and their related submenus for display
    menus = Menu.objects.prefetch_related('submenus').all()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('view_vendor_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserForm()
    return render(request, 'vendor/vendor_reg.html', {'form': form, 'menus': menus})

def create_vendor_details(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    if request.method == 'POST':
        form = VendorRegisterForm(request.POST, request.FILES)  # Added request.FILES for file uploads if needed
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user_id = id  # Associate the user
            vendor.save()
            form.save_m2m()  # Save the many-to-many field for materials
            return redirect('view_vendor_list')  # Redirect to vendor list after successful submission
    else:
        form = VendorRegisterForm()

    return render(request, 'vendor/add_vendor_details.html', {'form': form, 'menus': menus})



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

    return render(request, 'vendor/view_vendor_list.html', context)

