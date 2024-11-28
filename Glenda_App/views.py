from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from Glenda_App.forms import MenuForm, SubMenuForm
from Glenda_App.models import Menu
from inventory_app.models import Finished_Goods_Stock, RawMaterialsStock
from production_app.models import water_Finished_Goods, damaged_Goods
from purchase_app.models import RawMaterials
from register_app.models import CustomUser, MenuPermissions
from vendor_app.models import vendor_register
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q  # Import Q here
from collections import OrderedDict

# Create your views here.

def customer_index(request):
    return render(request,'front/index.html')


@login_required
def index(request):
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


    vendor=vendor_register.objects.all()

    vendor_count = vendor_register.objects.count()
    goods = water_Finished_Goods.objects.count()
    da = damaged_Goods.objects.count()
    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': sorted_allocated_menus,

        'vendor': vendor_count,
        'goods': goods,
        'da': da,
        'ven':vendor,
        'labels':la,
        'data':tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }

    return render(request, 'index.html', context)




def raw_materials_data(request):
    raw_materials = RawMaterials.objects.all()
    data = [
        {
            'name': material.name,
            'total_stock': material.total_stock
        }
        for material in raw_materials
    ]
    return JsonResponse(data, safe=False)

def calendar(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    return render(request, 'calendar.html', {'menus': menus})

def create_menu(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_menu')  # Change to redirect to index after creation
    else:
        form = MenuForm()
    return render(request, 'create_menu.html', {'form': form,'allocated_menus':allocated_menus})

def create_submenu(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    if request.method == 'POST':
        form = SubMenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_submenu')  # Change to redirect to index after creation
    else:
        form = SubMenuForm()
    return render(request, 'create_submenu.html', {'form': form,'allocated_menus':allocated_menus})


# views.py
# import matplotlib.pyplot as plt
# from io import BytesIO
# from django.http import HttpResponse
# from purchase_app.models import RawMaterials
# from inventory_app.models import Finished_Goods_Stock
#
# def pie_chart_view(request):
#     # Example: Fetch raw materials and stock data from the database
#     raw_materials = RawMaterials.objects.all()
#     names = [material.name for material in raw_materials]
#     stocks = [material.total_stock for material in raw_materials]
#
#     # Generate the pie chart
#     plt.figure(figsize=(7, 7))
#     plt.pie(stocks, labels=names, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
#     plt.title('Raw Materials Stock Distribution')
#     plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
#
#     # Save the plot to a BytesIO object
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close()
#
#     # Return the image as an HTTP response
#     buffer.seek(0)
#     return HttpResponse(buffer, content_type='image/png')
#
# from io import BytesIO
# import base64
#

# def daily_stock_bar_chart_image(request):
# #     # Get stock data ordered by date
# #     stock_data = Finished_Goods_Stock.objects.all().order_by('date')
# #
# #     # Get unique dates and corresponding stock values
# #     dates = [stock.date for stock in stock_data]
# #     stock_values = [stock.stock for stock in stock_data]
# #
# #     # Create the bar chart
# #     plt.figure(figsize=(10, 6))
# #     plt.bar(dates, stock_values, color='blue')
# #
# #     # Add labels and title
# #     plt.xlabel('Date')
# #     plt.ylabel('Stock Quantity')
# #     plt.title('Daily Water Stock')
# #
# #     # Convert the plot to an image
# #     buffer = BytesIO()
# #     plt.savefig(buffer, format='png')
# #     buffer.seek(0)
# #     plt.close()
# #
# #     # Return the image as an HTTP response
# #     return HttpResponse(buffer, content_type='image/png')


# def stock_data(request):
#     # Query data
#     finished_goods = water_Finished_Goods.objects.all()
#     raw_materials = RawMaterialsStock.objects.all()
#
#     # Prepare data
#     finished_goods_data = {
#         "names": [item.name for item in finished_goods],
#         "stock": [item.total_stock for item in finished_goods],
#     }
#
#     raw_materials_data = {
#         "names": [item.raw_materials.name for item in raw_materials],
#         "stock": [item.stock for item in raw_materials],
#     }
#
#     return JsonResponse({
#         "finished_goods": finished_goods_data,
#         "raw_materials": raw_materials_data,
#     })


# @login_required
# def user_list(request):
#     menus = Menu.objects.prefetch_related('submenus').all()
#     users = CustomUser.objects.filter(is_staff=True, is_superuser=False).exclude(id=request.user.id)
#     return render(request, 'chat/user_list.html', {'users': users,'menus':menus})
#
#
#
#
# # View to display chat with a specific user
# @login_required
# def chat_with_user(request, user_id):
#     menus = Menu.objects.prefetch_related('submenus').all()
#
#     user_to_chat = get_object_or_404(CustomUser, id=user_id)
#
#     # Fetching messages between the logged-in user and the selected user
#     messages = Message.objects.filter(
#         (Q(sender=request.user) & Q(receiver=user_to_chat)) |
#         (Q(sender=user_to_chat) & Q(receiver=request.user))
#     ).order_by('timestamp')  # Fetching messages between users
#
#     return render(request, 'chat/chat.html', {
#         'user': user_to_chat,'menus':menus,
#         'messages': messages  # Pass messages to the template
#     })
#
# # Function to send a message via POST request (API endpoint)
# @csrf_exempt  # Only use this for testing. Implement CSRF protection properly in production.
# def send_message(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         message_content = data.get('message')
#         user_id = data.get('user_id')
#
#         # Create and save the message
#         receiver = get_object_or_404(CustomUser, id=user_id)
#         message = Message.objects.create(
#             sender=request.user,
#             receiver=receiver,
#             content=message_content
#         )
#
#         return JsonResponse({
#             'status': 'success',
#             'message': 'Message sent',
#             'message_id': message.id,
#             'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Include the formatted timestamp
#         })
#
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def accounts_index(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': allocated_menus,
        'labels': la,
        'data': tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }
    return render(request,'index/accounts_index.html',context)

def sales_index(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': allocated_menus,
        'labels': la,
        'data': tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }
    return render(request,'index/sales_index.html',context)

def production_index(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': allocated_menus,
        'labels': la,
        'data': tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }
    return render(request,'index/production_index.html',context)

def logistics_index(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': allocated_menus,
        'labels': la,
        'data': tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }
    return render(request,'index/logistics_index.html',context)



def Inventory_index(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': allocated_menus,
        'labels': la,
        'data': tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }

    return render(request,'index/inventory_index.html',context)


def Hr_index(request):
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)




    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': allocated_menus,
        'labels': la,
        'data': tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }


    return render(request,'index/hr_index.html',context)

def management_index(request):
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


    raw_materials = RawMaterials.objects.all()
    la = [material.name for material in raw_materials]
    tt = [material.total_stock for material in raw_materials]
    # Get today's date
    today = timezone.now().date()

    # Define the last 7 days for the line chart
    dates = [today - timedelta(days=i) for i in range(7)]

    # Fetch finished goods stock data for the last 7 days
    daily_stock_summary = Finished_Goods_Stock.objects.filter(date__gte=today - timedelta(days=6)).values(
        'date').annotate(total_stock=Sum('stock')).order_by('date')

    # Prepare data for the chart
    labels = []
    data = []

    # Fill the labels and data with zeros for days without stock entries
    for date in dates:
        total_stock = 0
        for entry in daily_stock_summary:
            if entry['date'] == date:
                total_stock = entry['total_stock'] or 0
                break
        labels.append(date.strftime('%Y-%m-%d'))  # Format date as needed
        data.append(total_stock)  # Use total stock or 0 if no entry

    # Prepare the context for rendering
    context = {
        'allocated_menus': sorted_allocated_menus,
        'labels': la,
        'data': tt,
        'chart_data': {
            'labels': labels,
            'data': data,
        },
    }

    return render(request,'index.html',context)

