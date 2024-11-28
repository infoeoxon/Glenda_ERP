from django.urls import path

from inventory_app import views

urlpatterns = [
    path('Raw_materials_view', views.raw_materials_view, name='Raw_materials_view'),
    path('finishedgoods_stock_view', views.finishedgoods_stock_view, name='finishedgoods_stock_view'),
    path('finishedgoods_stock_history/<int:id>', views.finishedgoods_stock_history, name='finishedgoods_stock_history'),
    path('damagedgoods_stock_view', views.damagedgoods_stock_view, name='damagedgoods_stock_view'),
    path('finished_goods_stock_history_pdf/<int:id>', views.finished_goods_stock_history_pdf, name='finished_goods_stock_history_pdf'),
    path('finishedgoods_stock_history_excel/<int:id>', views.finishedgoods_stock_history_excel, name='finishedgoods_stock_history_excel'),
    path('raw_materials_stock_history/<int:id>', views.raw_materials_stock_history, name='raw_materials_stock_history'),
    path('raw_materials_history_pdf/<int:id>', views.raw_materials_stock_pdf, name='raw_materials_history_pdf'),
    path('damagedgoods_stock_history/<int:id>',views.damagedgoods_stock_history,name='damagedgoods_stock_history'),
    path('generate-pdf/<int:id>', views.generate_pdf, name='generate_pdf'),
    path('damaged_stock_history_excel/<int:id>',views.damaged_stock_history_excel,name='damaged_stock_history_excel'),
    path('finishedgoods_search_and_export', views.finishedgoods_search_and_export, name='finishedgoods_search_and_export'),
    path('finishedgoods_message_request',views.finishedgoods_message_request,name='finishedgoods_message_request'),
    path('damaged_goods_export_and_search', views.damaged_goods_export_and_search, name='damaged_goods_export_and_search'),
    path('raw_material_search_and_export', views.raw_material_search_and_export, name='raw_material_search_and_export'),
    path('raw_material_message_request', views.raw_material_message_request, name='raw_material_message_request'),
    path('raw_material_request_list', views.raw_material_request_list, name='raw_material_request_list'),
    path('raw_materials_stock_excel/<int:id>', views.raw_materials_stock_excel, name='raw_materials_stock_excel'),
    path('finishedgoods_request_messages_list', views.finishedgoods_request_messages_list, name='finishedgoods_request_messages_list'),
    path('raw_material_allocate/<int:id>', views.raw_material_allocate, name='raw_material_allocate'),
    path('raw_material_allocate_history/<int:id>', views.raw_material_allocate_history, name='raw_material_allocate_history'),
    path('raw_material_allocate_excel/<int:id>', views.raw_material_allocate_excel, name='raw_material_allocate_excel'),
    path('raw_materials_stock_allocate_pdf/<int:id>', views.raw_materials_stock_allocate_pdf, name='raw_materials_stock_allocate_pdf'),
    path('finished_goods_allocate/<int:id>', views.finished_goods_allocate, name='finished_goods_allocate'),
    path('finished_goods_allocate_history/<int:id>', views.finished_goods_allocate_history, name='finished_goods_allocate_history'),
    path('finished_goods_allocate_excel/<int:id>', views.finished_goods_allocate_excel, name='finished_goods_allocate_excel'),
    path('finished_goods_stock_allocate_pdf/<int:id>', views.finished_goods_stock_allocate_pdf, name='finished_goods_stock_allocate_pdf'),
    path('finishedgoods_message_request_list_pdf', views.finishedgoods_message_request_list_pdf, name='finishedgoods_message_request_list_pdf'),
    path('finishedgoods_message_request_list_excel', views.finishedgoods_message_request_list_excel, name='finishedgoods_message_request_list_excel'),

    path('inbox', views.inbox, name='inbox'),
    path('stock_verification', views.stock_verification, name='stock_verification'),

    path('demo_inventory_overview', views.demo_inventory_overview,name='demo_inventory_overview'),
    path('demo_request_list', views.demo_request_list, name='demo_request_list'),
    path('demo_all_inventory_history', views.demo_all_inventory_history, name='demo_all_inventory_history'),
    path('demo_request_list_history', views.demo_request_list_history, name='demo_request_list_history'),
    path('demo_stock_history', views.demo_stock_history, name='demo_stock_history'),
    path('demo_arrived_stock_verification_history', views.demo_arrived_stock_verification_history, name='demo_arrived_stock_verification_history'),

]