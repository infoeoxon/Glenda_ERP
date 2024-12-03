


from django.urls import path

from purchase_app import views

urlpatterns = [
    path('add_category',views.add_category,name='add_category'),
    path('create_raw_material',views.create_raw_material,name='create_raw_material'),
    path('view_rawmaterials',views.view_rawmaterials,name='view_rawmaterials'),
    path('update_rawmaterials/<int:id>', views.update_rawmaterials, name='update_rawmaterials'),
    path('delete_raw/<int:id>', views.delete_rawmaterils, name='delete_raw'),
    path('message_requests', views.message_request, name='message_requests'),
    path('message_response/<int:id>', views.message_response, name='message_response'),
    path('raw_material_purchase_search', views.raw_material_purchase_search, name='raw_material_purchase_search'),
    path('add_stocks/<int:id>', views.add_stocks, name='add_stocks'),
    path('rawmaterials_stock_history/<int:id>', views.rawmaterials_stock_history, name='rawmaterials_stock_history'),
    path('message_request_list_history', views.message_request_list_history, name='message_request_list_history'),
    path('raw_message_request_list_history_pdf', views.raw_message_request_list_history_pdf, name='raw_message_request_list_history_pdf'),
    path('raw_message_request_list_history_excel', views.raw_message_request_list_history_excel,name='raw_message_request_list_history_excel'),
    path('raw_materials_purchase_history_pdf/<int:id>', views.raw_materials_purchase_history_pdf,name='raw_materials_purchase_history_pdf'),
    path('raw_materials_purchase_history_excel/<int:id>', views.raw_materials_purchase_history_excel,name='raw_materials_purchase_history_excel'),

    path('demo_rfq', views.demo_rfq, name='demo_rfq'),
    path('demo_quotations', views.demo_quotations, name='demo_quotations'),
    path('demo_purchase_order_list', views.demo_purchase_order_list, name='demo_purchase_order_list'),
    path('demo_purchase_order', views.demo_purchase_order, name='demo_purchase_order'),
    path('demo_dispatch_notification', views.demo_dispatch_notification, name='demo_dispatch_notification'),
    path('demo_vendor_list', views.demo_vendor_list, name='demo_vendor_list'),
    path('demo_add_vendor', views.demo_add_vendor, name='demo_add_vendor'),
    path('demo_all_history', views.demo_all_history, name='demo_all_history'),
    path('demo_quotation_verification_history', views.demo_quotation_verification_history,name='demo_quotation_verification_history'),
    path('demo_add_vendor_history', views.demo_add_vendor_history, name='demo_add_vendor_history'),
    path('demo_rfq_history', views.demo_rfq_history, name='demo_rfq_history'),
    path('demo_purchase_order_history', views.demo_purchase_order_history, name='demo_purchase_order_history'),
    path('demo_dispatch_notification_history', views.demo_dispatch_notification_history, name='demo_dispatch_notification_history'),
    path('demo_new_rfq', views.demo_new_rfq, name='demo_new_rfq'),
    path('demo_inventory_request', views.demo_inventory_request, name='demo_inventory_request'),
    path('demo_vendor_year_report', views.demo_vendor_year_report, name='demo_vendor_year_report'),
    path('demo_req_from_inventory_report', views.demo_req_from_inventory_report, name='demo_req_from_inventory_report'),
    path('create_rfq_raw_materials', views.create_rfq_raw_materials, name='create_rfq_raw_materials'),
    path('update_quotation_status/<int:quotation_id>/<str:status>/', views.update_status, name='update_quotation_status'),
    path('create_po/<int:quotation_id>/', views.create_po, name='create_po'),
]
