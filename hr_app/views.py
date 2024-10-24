from django.shortcuts import render,redirect,get_object_or_404
from register_app.models import CustomUser
from hr_app.models import EmployeeDetails
from Glenda_App.models import Menu
from .forms import EmployeeDetailsForm
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa
import csv
def Employee_list(request):
    # Fetch all users with is_staff=True
    users = CustomUser.objects.filter(is_staff=True,is_superuser=False)

    for user in users:

        user.details_added = EmployeeDetails.objects.filter(user=user).exists()

    menus = Menu.objects.prefetch_related('submenus').all()

    # Pass the filtered HR employee details and menus to the context
    context = {
        'menus': menus,
        'users':users
    }

    return render(request, 'hr/Employee_list.html', context)

def AddDetails(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    if request.method == 'POST':
        form = EmployeeDetailsForm(request.POST, request.FILES)
        emergency_contact_number = request.POST.get('emergency_contact_number')
        aadhar_no = request.POST.get('aadhar_no')

        if len(str(emergency_contact_number)) != 10:
            messages.warning(request, 'Contact number must be exactly 10 digits.')

        if len(str(aadhar_no)) != 12:
            messages.warning(request, 'Aadhar number must be exactly 12 digits.')

        if EmployeeDetails.objects.filter(aadhar_no=aadhar_no).exists():
            messages.warning(request, 'Aadhar number already existed')
            return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

        if EmployeeDetails.objects.filter(emergency_contact_number=emergency_contact_number).exists():
            messages.warning(request, 'Phone number already existed')
            return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

        if form.is_valid():
            employee = form.save()
            employee.user_id = id  # Associate the user
            employee.save()
            return redirect('Employee_list')  # Redirect to vendor list after successful submission
    else:
        form = EmployeeDetailsForm()

    return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

def view_employee_profile(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    view = EmployeeDetails.objects.filter(user_id=id)

    return render(request,'hr/view_employee_profile.html',{'view':view,'menus':menus})

def update_employee_details(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()
    view = get_object_or_404(EmployeeDetails, id=id)

    if request.method == 'POST':
        form = EmployeeDetailsForm(request.POST,instance=view)

        if form.is_valid():
                form.save()
                return redirect('Employee_list')

    else:
        form = EmployeeDetailsForm(request.POST, instance=view)
    return render(request, 'hr/update_employee_details.html', {'view':view, 'menus': menus,'form':form})

def delete_employee_details(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Fetch the object or return a 404 error if not found
    dtl = get_object_or_404(EmployeeDetails, id=id)

    if request.method == "POST":
        dtl.delete()
        return redirect('Employee_list')

    # Render the confirmation page for GET requests
    return render(request, 'hr/delete_employee_details.html', {'dtl': dtl,'menus':menus})


def employee_search_and_export(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Start with an empty query to show all staff members by default
    employee_list = CustomUser.objects.filter(is_staff=True, is_superuser=False)

    search_query = request.GET.get('search_query', '').strip()
    export_format = request.GET.get('export', '')

    if search_query:
        filters = Q(is_staff=True, is_superuser=False)
        if search_query.isdigit():
            filters &= Q(phone_number__icontains=search_query)
        else:
            filters &= Q(name__icontains=search_query)

        employee_list = CustomUser.objects.filter(filters)

    # Check for export format (either 'csv' or 'pdf')
    if export_format == 'csv':
        # CSV export
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="employee_list.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone Number'])

        for employee in employee_list:
            writer.writerow([employee.name, employee.email, employee.phone_number])

        return response

    elif export_format == 'pdf':
        # PDF export
        template = get_template('hr/employee_details_pdf.html')  # A separate template for PDF
        context = {'users': employee_list, 'menus': menus}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="employee_list.pdf"'

        pdf_status = pisa.CreatePDF(html, dest=response)

        if pdf_status.err:
            return HttpResponse('Error generating PDF', status=500)

        return response

    # Normal page rendering (with search functionality)
    context = {
        'users': employee_list,  # Filtered employees list
        'menus': menus,
    }

    return render(request, 'hr/Employee_list.html', context)