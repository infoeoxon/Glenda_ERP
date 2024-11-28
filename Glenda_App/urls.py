

from django.urls import path,include

from Glenda_App import views
from Glenda_App.views import raw_materials_data

urlpatterns = [
    path('', views.customer_index, name='customer_index'),
    path('admin_home',views.index,name='admin_home'),
    path('create_menu', views.create_menu, name='create_menu'),
    path('create_submenu', views.create_submenu, name='create_submenu'),
    path('calendar', views.calendar, name='calendar'),
    # path('pie-chart/', views.pie_chart_view, name='pie_chart'),
    path('api/raw-materials/', raw_materials_data, name='raw_materials_data'),  # API endpoint
    # path('stock-data/', stock_data, name='stock_data'),
    # path('chat',views.user_list, name='user_list'),
    # path('chat/users/<int:user_id>/',views.chat_with_user, name='chat_with_user'),
    # path('chat/send_message/', views.send_message, name='send_message'),  # API endpoint for sending message
    path('accounts_index', views.accounts_index, name='accounts_index'),
    path('sales_index', views.sales_index, name='sales_index'),
    path('production_index', views.production_index, name='production_index'),
    path('logistics_index', views.logistics_index, name='logistics_index'),
    path('Inventory_index', views.Inventory_index, name='Inventory_index'),
    path('Hr_index', views.Hr_index, name='Hr_index'),
    path('management_index', views.management_index, name='management_index'),

]
