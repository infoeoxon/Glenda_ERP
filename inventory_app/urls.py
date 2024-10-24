

from django.urls import path

from inventory_app import views

urlpatterns = [
    path('Raw_materials_view', views.raw_materials_view, name='Raw_materials_view'),
    path('update_stocks/<int:id>', views.update_stocks, name='update_stocks'),
    path('finishedgoods_stock_view', views.finishedgoods_stock_view, name='finishedgoods_stock_view'),
    path('update_finished_goods_stocks/<int:id>', views.update_finished_goods_stocks, name='update_finished_goods_stocks'),
    path('finishedgoods_stock_history/<int:id>', views.finishedgoods_stock_history, name='finishedgoods_stock_history'),
    path('damagedgoods_stock_view', views.damagedgoods_stock_view, name='damagedgoods_stock_view'),
    path('update_damaged_goods_stocks/<int:id>', views.update_damaged_goods_stocks, name='update_damaged_goods_stocks'),
    path('finishedgoods_stock_history_pdf/<int:id>', views.finishedgoods_stock_history_pdf, name='finishedgoods_stock_history_pdf'),
    path('finishedgoods_stock_history_excel', views.finished_goods_stock_history_excel, name='finishedgoods_stock_history_excel'),
    path('raw_materials_stock_history/<int:id>', views.raw_materials_stock_history, name='raw_materials_stock_history'),
    path('raw_materials_history_pdf/<int:id>', views.raw_materials_stock_pdf, name='raw_materials_history_pdf'),
    path('damagedgoods_stock_history/<int:id>',views.damagedgoods_stock_history,name='damaged_good_stock_history'),
    path('generate-pdf/<int:id>', views.generate_pdf, name='generate_pdf'),
    path('generate_full_pdf',views.generate_full_pdf,name='generate_full_pdf'),
    path('damaged_stock_history_excel',views.damaged_stock_history_excel,name='damaged_stock_history_excel'),
    path('generate_excel',views.generate_excel,name='generate_excel'),
    path('search',views.search,name='search'),
    path('finishedgoods_search_and_export', views.finishedgoods_search_and_export, name='finishedgoods_search_and_export'),
    path('finishedgoods_message_request',views.finishedgoods_message_request,name='finishedgoods_message_request'),
    path('damaged_search',views.damaged_search,name='damaged_search'),
    path('raw_material_search', views.raw_material_search, name='raw_material_search'),
    path('raw_material_message_request', views.raw_material_message_request, name='raw_material_message_request'),
    path('raw_material_request_list', views.raw_material_request_list, name='raw_material_request_list'),
    path('raw_materials_stock_excel', views.raw_materials_stock_excel, name='raw_materials_stock_excel'),
    path('finishedgoods_request_messages_list', views.finishedgoods_request_messages_list, name='finishedgoods_request_messages_list'),

]

