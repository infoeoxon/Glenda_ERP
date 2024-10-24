import csv
import io

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from Glenda_App.models import Menu


from inventory_app.forms import Raw_materials_StockForm, Finished_Goods_StockForm,Finished_Goods_RequestForm,Damaged_Goods_StockForm,Raw_materials_requestForm
from inventory_app.models import RawMaterialsStock,Finished_Goods_Stock,Finished_Goods_Request,Damaged_Goods_Stock,Raw_material_request
from production_app.models import water_Finished_Goods,water_Finished_goods_category,damaged_Goods,Damaged_good_category
from register_app.models import department
from purchase_app.models import RawMaterials,RawMaterialCategory
from Glenda_App.models import Menu
from xhtml2pdf import pisa
from django.db.models import Q
from openpyxl.styles import Font,Alignment
from openpyxl import Workbook
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.db.models import Sum

# Create your views here.




def raw_materials_view(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    raw_materials = RawMaterials.objects.prefetch_related('stocks').all()
    categories = RawMaterialCategory.objects.all()


    # Calculate total stock for each raw material
    total_stocks = {
        material.id: material.stocks.aggregate(total=Sum('stock'))['total'] or 0
        for material in raw_materials
    }

    return render(request, 'inventory/view_raw_materials.html', {'view': raw_materials, 'menus': menus, 'total_stocks': total_stocks,'categories':categories})

def update_stocks(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()
    raw_material = get_object_or_404(RawMaterials, id=id)

    if request.method == 'POST':
        form = Raw_materials_StockForm(request.POST)
        if form.is_valid():
            stock_entry = form.save(commit=False)
            stock_entry.raw_materials = raw_material  # Set the raw material
            stock_entry.save()  # Save the new stock entry

            # Update the total stock for the raw material
            total_stock = raw_material.stocks.aggregate(total=Sum('stock'))['total'] or 0
            raw_material.total_stock = total_stock
            raw_material.save()  # Save the updated total stock

            return redirect('Raw_materials_view')  # Redirect to the list view
    else:
        form = Raw_materials_StockForm()

    return render(request, 'inventory/add_stock.html', {
        'form': form,
        'menus': menus,
        'raw_material': raw_material
    })




def update_finished_goods_stocks(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()
    finished_goods = get_object_or_404(water_Finished_Goods, id=id)

    if request.method == 'POST':
        form = Finished_Goods_StockForm(request.POST)
        if form.is_valid():
            stock_entry = form.save(commit=False)
            stock_entry.finished_goods = finished_goods  # Set the raw material
            stock_entry.save()  # Save the new stock entry

            # Update the total stock for the raw material
            total_stock = finished_goods.stocks.aggregate(total=Sum('stock'))['total'] or 0
            finished_goods.total_stock = total_stock
            finished_goods.save()  # Save the updated total stock

            return redirect('finishedgoods_stock_view')  # Redirect to the list view
    else:
        form = Finished_Goods_StockForm()

    return render(request, 'inventory/add_finishedgoods_stock.html', {
        'form': form,
        'menus': menus,
        'finished_goods': finished_goods
    })


def finishedgoods_stock_view(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    finished_goods = water_Finished_Goods.objects.prefetch_related('stocks').all()
    categories = water_Finished_goods_category.objects.all()

    # Calculate total stock for each raw material
    total_stocks = {
        material.id: material.stocks.aggregate(total=Sum('stock'))['total'] or 0
        for material in finished_goods
    }

    return render(request, 'inventory/view_finished_goods.html', {'view': finished_goods, 'menus': menus, 'total_stocks': total_stocks,'categories':categories})


def finishedgoods_stock_history(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()
    finished_good = Finished_Goods_Stock.objects.filter(finished_goods_id=id)
    print(finished_good)


    return render(request,'inventory/view_finished_goods_history.html',{'data':finished_good,'menus': menus})

def update_damaged_goods_stocks(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()
    damaged_goods = get_object_or_404(damaged_Goods, id=id)

    if request.method == 'POST':
        form = Damaged_Goods_StockForm(request.POST)
        if form.is_valid():
            stock_entry = form.save(commit=False)
            stock_entry.damaged = damaged_goods  # Set the raw material
            stock_entry.save()  # Save the new stock entry

            # Update the total stock for the raw material
            total_stock = damaged_goods.stocks.aggregate(total=Sum('stock'))['total'] or 0
            damaged_goods.total_stock = total_stock
            damaged_goods.save()  # Save the updated total stock

            return redirect('damagedgoods_stock_view')  # Redirect to the list view
    else:
        form = Damaged_Goods_StockForm()

    return render(request, 'inventory/add_damage_stock.html', {
        'form': form,
        'menus': menus,
        'damaged_goods': damaged_goods
    })


def damagedgoods_stock_view(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    damaged_goods = damaged_Goods.objects.prefetch_related('stocks').all()

    # Calculate total stock for each raw material
    total_stocks = {
        material.id: material.stocks.aggregate(total=Sum('stock'))['total'] or 0
        for material in damaged_goods
    }

    return render(request, 'inventory/view_damaged_goods.html', {'view': damaged_goods, 'menus': menus, 'total_stocks': total_stocks})


def finishedgoods_stock_history(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()
    finished_good = Finished_Goods_Stock.objects.filter(finished_goods_id=id)
    print(finished_good)
    context = {
        'data': finished_good,
        'menus': menus,
        'id': id
    }


    return render(request,'inventory/view_finished_goods_history.html',context)

def finishedgoods_stock_history_pdf(request, id):
    view = Finished_Goods_Stock.objects.filter(finished_goods_id=id).first()
    filename = f"{view.finished_goods.category.category_name}_inventory_report.pdf"

    finished_good = Finished_Goods_Stock.objects.filter(finished_goods_id=id)
    context = {'view': finished_good, 'name':view}

    template = get_template('inventory/finishedgoods_stock_pdf.html')
    html = template.render(context)

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pdf_status = pisa.CreatePDF(
        html,
        dest=response
    )
    return response



def finished_goods_stock_history_excel(request):
    # Create a Workbook
    wb = Workbook()
    ws = wb.active

    # Write a headline row that spans all columns
    ws.merge_cells('A1:E1')  # Adjust based on your number of columns (5 in this case)
    ws['A1'] = 'Finished Goods Stock History'

    # Set font properties including bold and increased font size
    headline_font = Font(bold=True, size=14)
    ws['A1'].font = headline_font

    # Center the headline text
    ws['A1'].alignment = Alignment(horizontal='center')

    # Write the header row
    headers = ['Category', 'Name', 'Size', 'Stock', 'Date']
    ws.append(headers)

    # Make header row bold
    header_font = Font(bold=True)
    for col_num, header in enumerate(headers, 1):  # Enumerate from 1 for Excel column indexes
        cell = ws.cell(row=2, column=col_num)  # Header is in row 2 (row 1 is the headline)
        cell.font = header_font

    # Retrieve all items from the database
    items = Finished_Goods_Stock.objects.all()

    # Write data rows
    for item in items:
        if item.finished_goods is not None:
            ws.append([
                item.finished_goods.category.category_name if item.finished_goods.category else 'N/A',  # Category name
                item.finished_goods.name,  # Item name
                item.finished_goods.size,  # Size
                item.stock,  # Total stock
                item.date.strftime('%Y-%m-%d') if item.date else 'N/A'  # Date formatted as 'YYYY-MM-DD'
            ])
        else:
            ws.append([
                'N/A',  # Category name if raw_materials is None
                'N/A',  # Name if raw_materials is None
                'N/A',  # Size if raw_materials is None
                item.stock,  # Total stock
                item.date.strftime('%Y-%m-%d') if item.date else 'N/A'  # Date formatted as 'YYYY-MM-DD'
            ])

    # Create an HTTP response with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="finished_goods_stock_history.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response



def raw_materials_stock_history(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()
    raw_materials = RawMaterialsStock.objects.filter(raw_materials_id=id)
    context = {
        'data': raw_materials,
        'menus': menus,
        'id': id
    }

    return render(request,'inventory/view_raw_materials_history.html',context)


def raw_materials_stock_pdf(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()
    view = RawMaterialsStock.objects.filter(raw_materials_id=id).first()
    data = RawMaterialsStock.objects.filter(raw_materials_id=id)
    context = {'view': data, 'menu': menus, 'name':view}

    template = get_template('inventory/raw_material_stock_pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{view.raw_materials.name}_raw_material.pdf"'

    pdf_status = pisa.CreatePDF(
        html,
        dest=response
    )
    return response


def raw_materials_stock_excel(request):
    # Create a Workbook
    wb = Workbook()
    ws = wb.active

    # Write a headline row that spans all columns
    ws.merge_cells('A1:E1')  # Adjust based on your number of columns (5 in this case)
    ws['A1'] = 'Raw Material Stock History'

    # Set font properties including bold and increased font size
    headline_font = Font(bold=True, size=14)
    ws['A1'].font = headline_font

    # Center the headline text
    ws['A1'].alignment = Alignment(horizontal='center')

    # Write the header row
    headers = ['Category', 'Name', 'Size', 'Stock', 'Date']
    ws.append(headers)

    # Make header row bold
    header_font = Font(bold=True)
    for col_num, header in enumerate(headers, 1):  # Enumerate from 1 for Excel column indexes
        cell = ws.cell(row=2, column=col_num)  # Header is in row 2 (row 1 is the headline)
        cell.font = header_font

    # Retrieve all items from the database
    items = RawMaterialsStock.objects.all()

    # Write data rows
    for item in items:
        if item.raw_materials is not None:
            ws.append([
                item.raw_materials.category.category_name if item.raw_materials.category else 'N/A',  # Category name
                item.raw_materials.name,  # Item name
                item.raw_materials.size,  # Size
                item.stock,  # Total stock
                item.date.strftime('%Y-%m-%d') if item.date else 'N/A'  # Date formatted as 'YYYY-MM-DD'
            ])
        else:
            ws.append([
                'N/A',  # Category name if raw_materials is None
                'N/A',  # Name if raw_materials is None
                'N/A',  # Size if raw_materials is None
                item.stock,  # Total stock
                item.date.strftime('%Y-%m-%d') if item.date else 'N/A'  # Date formatted as 'YYYY-MM-DD'
            ])

    # Create an HTTP response with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="raw_material_stock_history.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response

def damagedgoods_stock_history(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()
    damaged_goods = Damaged_Goods_Stock.objects.filter(damaged_id=id)
    print("success")

    return render(request,'inventory/damaged_stock_history.html',{'menus':menus,'data':damaged_goods,'id':id})


def generate_pdf(request,id):
    view = Damaged_Goods_Stock.objects.filter(damaged_id=id).first()
    filename = f"{view.damaged.category.category_name}_inventory_report.pdf"

    damaged = Damaged_Goods_Stock.objects.filter(damaged_id=id)
    context = {'view': damaged, 'name': view}

    template = get_template('inventory/damaged_stock_pdf.html')
    html = template.render(context)

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pdf_status = pisa.CreatePDF(
        html,
        dest=response
    )
    return response

def damaged_stock_history_excel(request):
    # Create a Workbook
    wb = Workbook()
    ws = wb.active

    # Write a headline row that spans all columns
    ws.merge_cells('A1:E1')  # Adjust based on your number of columns (5 in this case)
    ws['A1'] = 'Damaged Stock History'

    # Set font properties including bold and increased font size
    headline_font = Font(bold=True, size=14)
    ws['A1'].font = headline_font

    # Center the headline text
    ws['A1'].alignment = Alignment(horizontal='center')

    # Write the header row
    headers = ['Category', 'Name', 'Description', 'Stock', 'Date']
    ws.append(headers)

    # Make header row bold
    header_font = Font(bold=True)
    for col_num, header in enumerate(headers, 1):  # Enumerate from 1 for Excel column indexes
        cell = ws.cell(row=2, column=col_num)  # Header is in row 2 (row 1 is the headline)
        cell.font = header_font

    # Retrieve all items from the database
    items = Damaged_Goods_Stock.objects.all()

    # Write data rows
    for item in items:
        if item.damaged is not None:
            ws.append([
                item.damaged.category.category_name if item.damaged.category else 'N/A',  # Category name
                item.damaged.name,  # Item name
                item.damaged.description,  # Size
                item.stock,  # Total stock
                item.date.strftime('%Y-%m-%d') if item.date else 'N/A'  # Date formatted as 'YYYY-MM-DD'
            ])
        else:
            ws.append([
                'N/A',  # Category name if raw_materials is None
                'N/A',  # Name if raw_materials is None
                'N/A',  # Size if raw_materials is None
                item.stock,  # Total stock
                item.date.strftime('%Y-%m-%d') if item.date else 'N/A'  # Date formatted as 'YYYY-MM-DD'
            ])

    # Create an HTTP response with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="damaged_stock_history.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response

def generate_full_pdf(request):
    view = Damaged_Goods_Stock.objects.all()
    filename = "full_analysis_report.pdf"

    damaged = Damaged_Goods_Stock.objects.all()
    context = {'view': damaged, 'name': view}

    template = get_template('inventory/damaged_full_stock_pdf.html')
    html = template.render(context)

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pdf_status = pisa.CreatePDF(
        html,
        dest=response
    )
    return response

def damaged_search(request):
    categories = Damaged_good_category.objects.all()
    damaged_goods_list = damaged_Goods.objects.all()
    menus = Menu.objects.prefetch_related('submenus').all()

    context = {
        'view': damaged_goods_list,  # This is the queryset for the table in the HTML
        'categories': categories,
        'menus':menus
    }

    # Handle search requests
    if request.method == 'GET':
        damaged_name = request.GET.get('name', None)
        damaged_category = request.GET.get('category', None)

        # Build filters
        filters = Q()

        # If the search name is provided, filter by the name in damaged_Goods
        if damaged_name:
            filters &= Q(name__icontains=damaged_name)

        # If a valid category is selected, filter by the category
        if damaged_category:
            filters &= Q(category_id=damaged_category)  # Use category_id to filter

        # Apply the filters to the queryset if filters are provided
        if filters:
            damaged_goods_list = damaged_Goods.objects.filter(filters)

        # Update the context with the filtered queryset
        context['view'] = damaged_goods_list

    return render(request, 'inventory/view_damaged_goods.html', context)



def generate_excel(request):
    # Create a Workbook
    wb = Workbook()
    ws = wb.active

    # Write a headline row that spans all columns
    ws.merge_cells('A1:D1')  # Adjust based on your number of columns
    ws['A1'] = 'Damaged Goods Stock List'

    # Set font properties including bold and increased font size
    headline_font = Font(bold=True, size=14)  # Set bold and font size to 14
    ws['A1'].font = headline_font  # Apply the font to the headline

    # Center the headline text
    ws['A1'].alignment = Alignment(horizontal='center')  # Center alignment

    # Write the header row
    ws.append([ 'Category', 'Name', 'Total Stock'])

    # Retrieve all items from the database
    items = Damaged_Goods_Stock.objects.all()

    # Write data rows
    for item in items:
        ws.append([
            item.damaged.category.category_name,  # Category name
            item.damaged.name,  # Item name
            item.stock  # Total stock
        ])

    # Create an HTTP response with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="damaged_goods_stock_list.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response


def search(request):
    items = []
    if request.method == "POST":
        search_obj = request.POST.get("search")
        if search_obj:
            items = damaged_Goods.objects.filter(
                Q(description__icontains=search_obj) | Q(name__icontains=search_obj)
            )
        else:
            data = "No search item"
    return render(request, 'inventory/searched_damaged_goods.html', {"items": items})



def finishedgoods_search_and_export(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Get search query parameters
    search_name = request.GET.get('name', '').strip()  # Get name from the query string
    search_category = request.GET.get('category', '').strip()  # Get category from the query string

    # Start by showing all finished goods if no search parameters are provided
    if not search_name and not search_category:
        finished_goods_list = water_Finished_Goods.objects.all()  # Show all data initially
    else:
        # If search filters are provided, apply them
        filters = Q()  # Initialize an empty filter

        if search_name:
            filters &= Q(name__icontains=search_name)  # Filter by name if provided

        if search_category and search_category.isdigit():
            filters &= Q(category_id=search_category)  # Filter by category if provided

        # Apply the filters to the queryset
        finished_goods_list = water_Finished_Goods.objects.filter(filters)

        # If no results match the search, return an empty queryset
        if not finished_goods_list.exists():
            finished_goods_list = water_Finished_Goods.objects.none()  # Return an empty queryset

    # Check if the request is for exporting to CSV (triggered by a specific URL parameter, e.g., 'export')
    if 'export' in request.GET:
        # Prepare the response for CSV download
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Finished-Goods-List.csv"'

        # Create a CSV writer
        writer = csv.writer(response)
        writer.writerow(['Category', 'Name', 'Size', 'Total Stock'])  # Header row

        # Write each finished good's details to the CSV
        for finished_good in finished_goods_list:
            writer.writerow([
                finished_good.category.category_name,
                finished_good.name,
                finished_good.size,
                finished_good.total_stock
            ])

        return response  # Return the CSV response for download

    # Otherwise, render the filtered search results to the template
    categories = water_Finished_goods_category.objects.all()  # Get all categories for the dropdown
    context = {
        'view': finished_goods_list,  # Pass the filtered finished goods list to the template
        'categories': categories,  # Pass the categories for the search dropdown
        'menus': menus,
        'search_name': search_name,  # Keep the search name in the context to display it in the form
        'search_category': search_category  # Keep the selected category in the context
    }

    return render(request, 'inventory/view_finished_goods.html', context)


def finishedgoods_request_messages_list(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    data = Finished_Goods_Request.objects.all()

    return render(request,'inventory/finishedgoods_request_message_list.html',{'data':data,'menus':menus})


def finishedgoods_message_request(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    dept = department.objects.all()
    category = water_Finished_goods_category.objects.all()
    name = water_Finished_Goods.objects.all()
    view = Finished_Goods_Request.objects.all()

    if request.method == 'POST':
        form = Finished_Goods_RequestForm(request.POST)
        print(request.POST)  # Debug: Print the form data
        if form.is_valid():
            print("Form is valid")  # Debug: Form is valid
            form_entry = form.save(commit=False)
            # Ensure foreign key is assigned correctly
            form_entry.name = form.cleaned_data['name']
            form_entry.status = 'Pending'
            form_entry.save()
            return redirect('finishedgoods_stock_view')
        else:
            print(form.errors)  # Debug: Print form errors
    else:
        form = Finished_Goods_RequestForm()

    return render(request, 'inventory/finishedgoods_message_request.html', {
        'form': form,
        'menus': menus,
        'department': dept,
        'category': category,
        'name': name,
        'view': view
    })



def raw_material_search(request):
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
            raw_materials = RawMaterials.objects.filter(filters)

            # Debugging: Logging or print statement
            print(f"Filters applied: {filters}")
            print(f"Filtered records count: {search_list.count()}")

        context['view'] = raw_materials # Filtered stock data

    return render(request, 'inventory/view_raw_materials.html', context)


def raw_material_request_list(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    message = Raw_material_request.objects.all()

    return render(request, 'inventory/raw_material_request_list.html', {'menus': menus, 'message':message})

def raw_material_message_request(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    dept = department.objects.all()
    category = RawMaterialCategory.objects.all()
    name= RawMaterials.objects.all()
    view = Raw_material_request.objects.all()


    if request.method == 'POST':
        form = Raw_materials_requestForm(request.POST)
        if form.is_valid():
            form_entry = form.save(commit=False)
            form_entry.name = form.cleaned_data['name']
            form_entry.status = 'Pending'
            form_entry.save()

        return redirect('raw_material_request_list')  # Redirect to the list view
    else:
        form = Raw_materials_requestForm()

    return render(request, 'inventory/raw_material_message_request.html', {
        'form': form,
        'menus': menus,
        'department': dept,
        'category': category,
        'name': name,
        'view':view}
)


